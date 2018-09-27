from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from youtube_dl import YoutubeDL
from .models import Track
from .serializers import TrackSerializer


class APIYouTube(APIView):
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
        'outtmpl': settings.BASE_DIR + '/media/documents/music/%(id)s.%(ext)s',
    }

    def get(self, request, format=None):
        url = request.data['url']
        idYoutube = url.split('watch?v=')[1]
        filePath = 'documents/music/{0}.mp3'.format(idYoutube)
        track = Track.objects.filter(file=filePath)
        if 'list=' in url:
            raise ValidationError({'detail': 'playlist does not support.'})
        if track.exists():
            serializer = TrackSerializer(track.first(),
                                         context={'request': request})
            return Response(serializer.data)
        try:
            with YoutubeDL(self.options) as ydl:
                info = ydl.extract_info(url, download=False)
                data = {
                    'id': info['id'],
                    'url': info['webpage_url'],
                    'title': info['title'],
                    'thumbnail': info['thumbnail']
                    }
            return Response(data)
        except Exception as e:
            raise NotFound()

    def post(self, request, format=None):
        user = request.user
        url = request.data['url']
        filePath = 'documents/music/{0}.mp3'.format(url.split('watch?v=')[1])
        if 'list=' in url:
            raise ValidationError({'detail': 'playlist does not support.'})
        if Track.objects.filter(file=filePath).exists():
            raise ValidationError({'detail': 'track exist'})
        try:
            with YoutubeDL(self.options) as ydl:
                info = ydl.extract_info(url, download=True)

            track = Track.objects.create(
                title=info['title'],
                thumbnail=info['thumbnail'],
                in_youtube=True,
                upload_by=user
            )
            track.file.name = 'documents/music/{0}.mp3'.format(info['id'])
            track.save()
            serializer = TrackSerializer(track, context={'request': request})
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        except:
            raise NotFound()
