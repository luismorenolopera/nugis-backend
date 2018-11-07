from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from youtube_dl import YoutubeDL
from .models import Track
from .serializers import TrackSerializer, YoutubeSetSerializer


class APIYouTube(APIView):
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
        'outtmpl': settings.MEDIA_ROOT + '/documents/music/%(id)s.%(ext)s',
    }
    id_get = openapi.Parameter(
        'id',
        openapi.IN_QUERY,
        description='id from a youtube video',
        type=openapi.TYPE_STRING
    )
    track_response = openapi.Response('Created', TrackSerializer)

    @swagger_auto_schema(manual_parameters=[id_get])
    def get(self, request):
        """
        Return basic info from a youtube video.
        """
        try:
            id = request.query_params['id']
        except Exception as e:
            raise ValidationError({'detail': 'id is required'})
        filePath = 'documents/music/{0}.mp3'.format(id)
        track = Track.objects.filter(file=filePath)
        url = 'https://www.youtube.com/watch?v={}'.format(id)
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

    @swagger_auto_schema(request_body=YoutubeSetSerializer,
                         responses={201: track_response})
    def post(self, request):
        """
        Download a video in the app, Return a track.
        """
        serializer = YoutubeSetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        id = serializer.data['id']
        user = request.user
        filePath = 'documents/music/{0}.mp3'.format(id)
        url = 'https://www.youtube.com/watch?v={}'.format(id)
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
