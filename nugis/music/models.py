from django.db import models
from django.db.models.signals import pre_save, post_delete, post_save
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from rest_framework.authtoken.models import Token
from mutagen.mp3 import MP3


class Album(models.Model):
    name = models.CharField(max_length=90)
    image = models.ImageField(upload_to='documents/images',
                              null=True,
                              blank=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Artist(models.Model):
    alias = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        if self.alias:
            return self.alias
        return self.first_name


class Track(models.Model):
    file = models.FileField(upload_to='documents/music')
    title = models.CharField(max_length=100)
    duration = models.PositiveSmallIntegerField(blank=True, null=True)
    in_youtube = models.BooleanField(default=False)
    thumbnail = models.URLField(default=None, blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    upload_by = models.ForeignKey(User,
                                  on_delete=models.SET_NULL,
                                  blank=True,
                                  null=True,
                                  related_name='tracks')
    album = models.ForeignKey(Album,
                              on_delete=models.CASCADE,
                              related_name='tracks',
                              blank=True,
                              null=True)
    artists = models.ManyToManyField(Artist,
                                     related_name='tracks',
                                     through='TrackArtist',
                                     through_fields=('track',
                                                     'artist'))
    genders = models.ManyToManyField(Genre,
                                     related_name='tracks',
                                     through='TrackGenre',
                                     through_fields=('track',
                                                     'gender'))

    def __str__(self):
        return self.title


class TrackArtist(models.Model):
    track = models.ForeignKey(Track,
                              on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist,
                               on_delete=models.CASCADE)

    def __str__(self):
        return '{0} : {1}'.format(self.track,
                                  self.artist)

    class Meta:
        unique_together = ('track', 'artist')


class TrackGenre(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    gender = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return '{0} : {1}'.format(self.track,
                                  self.gender)

    class Meta:
        unique_together = ('track', 'gender')


class PlayList(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='playlists')
    tracks = models.ManyToManyField(Track,
                                    through='PlayListTrack',
                                    through_fields=('playlist',
                                                    'track'))

    def __str__(self):
        return self.name


class PlayListTrack(models.Model):
    playlist = models.ForeignKey(PlayList, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)

    def __str__(self):
        return '{0} : {1}'.format(self.playlist,
                                  self.track)

    class Meta:
        unique_together = ('playlist', 'track')


@receiver(pre_save, sender=Track)
def get_duration(sender, instance, **kwargs):
    """Get the duration of a track before saving it."""
    if instance.file:
        track = MP3(instance.file)
        instance.duration = int(track.info.length)


@receiver(post_delete, sender=Track)
def delete_track(sender, instance, **kwargs):
    """Delete the file from a track after delete the track."""
    instance.file.delete(False)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Token for DRF."""
    if created:
        Token.objects.create(user=instance)
