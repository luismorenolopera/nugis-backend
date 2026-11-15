import shutil
import tempfile
from unittest import mock

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework.test import APITestCase

from .models import PlayList, PlayListTrack, Track

MEDIA = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA)
class BaseTest(APITestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA, ignore_errors=True)

    def setUp(self):
        self.alice = User.objects.create_user('alice', password='Wake-up-2077')
        self.bob = User.objects.create_user('bob', password='Wake-up-2077')
        self.client.force_authenticate(self.alice)

    def mp3(self, content_type='audio/mpeg'):
        return SimpleUploadedFile('song.mp3', b'ID3' + b'\x00' * 64,
                                  content_type=content_type)

    def make_track(self, owner, title='Track'):
        track = Track(title=title, upload_by=owner)
        track.file.save('t.mp3', self.mp3(), save=False)
        track.save()
        return track


class TrackTests(BaseTest):
    def test_requires_auth(self):
        self.client.force_authenticate(None)
        self.assertEqual(self.client.get('/music/tracks/').status_code, 401)

    def test_upload_accepts_audio_mpeg(self):
        res = self.client.post('/music/tracks/', {
            'title': 'Night City', 'file': self.mp3('audio/mpeg')},
            format='multipart')
        self.assertEqual(res.status_code, 201, res.data)
        self.assertEqual(Track.objects.get().upload_by, self.alice)

    def test_upload_rejects_other_types(self):
        res = self.client.post('/music/tracks/', {
            'title': 'x', 'file': SimpleUploadedFile('x.txt', b'hi', 'text/plain')},
            format='multipart')
        self.assertEqual(res.status_code, 400)

    def test_list_and_search(self):
        self.make_track(self.bob, 'Chrome Heart')
        self.make_track(self.bob, 'Neon Rain')
        res = self.client.get('/music/tracks/?search=neon')
        self.assertEqual(res.data['count'], 1)
        self.assertEqual(res.data['results'][0]['title'], 'Neon Rain')

    def test_only_uploader_can_edit_or_delete(self):
        track = self.make_track(self.bob)
        url = '/music/tracks/{}/'.format(track.pk)
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertEqual(self.client.patch(url, {'title': 'x'}).status_code, 403)
        self.assertEqual(self.client.delete(url).status_code, 403)
        self.client.force_authenticate(self.bob)
        self.assertEqual(self.client.delete(url).status_code, 204)


class PlaylistTests(BaseTest):
    def test_playlists_are_private(self):
        PlayList.objects.create(name='Bob mix', owner=self.bob)
        mine = self.client.post('/music/playlists/', {'name': 'Synthwave'})
        self.assertEqual(mine.status_code, 201)
        names = [p['name'] for p in self.client.get('/music/playlists/').data]
        self.assertEqual(names, ['Synthwave'])

    def test_set_track_playlists(self):
        track = self.make_track(self.bob)
        p1 = PlayList.objects.create(name='a', owner=self.alice)
        p2 = PlayList.objects.create(name='b', owner=self.alice)
        res = self.client.post('/music/playlists/track',
                               {'track': track.pk, 'playlists': [p1.pk, p2.pk]},
                               format='json')
        self.assertEqual(res.status_code, 201)
        got = self.client.get('/music/playlists/track?id={}'.format(track.pk)).data
        self.assertEqual(sorted(x['playlist'] for x in got), [p1.pk, p2.pk])

    def test_playlist_does_not_leak_user_data(self):
        track = self.make_track(self.bob)
        pl = PlayList.objects.create(name='a', owner=self.alice)
        pl.tracks.add(track)
        res = self.client.get('/music/playlists/{}/'.format(pl.pk))
        self.assertEqual(res.data['tracks'][0]['title'], 'Track')
        self.assertNotIn('password', str(res.content))
        self.assertTrue(res.data['tracks'][0]['file'].startswith('http'))

    def test_cannot_add_to_someone_elses_playlist(self):
        track = self.make_track(self.alice)
        theirs = PlayList.objects.create(name='bob', owner=self.bob)
        res = self.client.post('/music/playlists/track',
                               {'track': track.pk, 'playlists': [theirs.pk]},
                               format='json')
        self.assertEqual(res.status_code, 400)
        self.assertFalse(PlayListTrack.objects.exists())


class CatalogTests(BaseTest):
    def test_catalog_read_only_for_non_staff(self):
        self.assertEqual(self.client.get('/music/genres/').status_code, 200)
        self.assertEqual(self.client.post('/music/genres/', {'name': 'x'}).status_code, 403)


class YoutubeTests(BaseTest):
    def test_rejects_invalid_id(self):
        self.assertEqual(self.client.get('/music/yt_upload?id=../../etc').status_code, 400)
        res = self.client.post('/music/yt_upload', {'id': 'bad id'}, format='json')
        self.assertEqual(res.status_code, 400)

    @mock.patch('music.APIyt.YoutubeDL')
    def test_info(self, ydl):
        ydl.return_value.__enter__.return_value.extract_info.return_value = {
            'id': 'dQw4w9WgXcQ', 'webpage_url': 'u', 'title': 'T',
            'thumbnail': 'http://img', 'duration': 10}
        res = self.client.get('/music/yt_upload?id=dQw4w9WgXcQ')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['title'], 'T')
