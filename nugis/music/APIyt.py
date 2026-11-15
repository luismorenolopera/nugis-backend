import os

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from yt_dlp import YoutubeDL

from .models import Track
from .serializers import TrackSerializer, YoutubeSetSerializer

TITLE_MAX_LENGTH = Track._meta.get_field('title').max_length


def ydl_options():
    return {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(settings.MEDIA_ROOT,
                                'documents/music/%(id)s.%(ext)s'),
    }


def track_path(video_id):
    return 'documents/music/{0}.mp3'.format(video_id)


def video_url(video_id):
    return 'https://www.youtube.com/watch?v={0}'.format(video_id)


class APIYouTube(APIView):
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
        serializer = YoutubeSetSerializer(data={'id': request.query_params.get('id', '')})
        if not serializer.is_valid():
            raise ValidationError({'detail': 'a valid id is required'})
        video_id = serializer.validated_data['id']
        track = Track.objects.filter(file=track_path(video_id)).first()
        if track:
            return Response(TrackSerializer(track, context={'request': request}).data)
        try:
            with YoutubeDL(ydl_options()) as ydl:
                info = ydl.extract_info(video_url(video_id), download=False)
        except Exception:
            raise NotFound()
        return Response({
            'id': info['id'],
            'url': info.get('webpage_url'),
            'title': info.get('title'),
            'thumbnail': info.get('thumbnail'),
            'duration': info.get('duration'),
        })

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
        video_id = serializer.validated_data['id']
        if Track.objects.filter(file=track_path(video_id)).exists():
            raise ValidationError({'detail': 'track exist'})
        try:
            with YoutubeDL(ydl_options()) as ydl:
                info = ydl.extract_info(video_url(video_id), download=True)
        except Exception:
            raise NotFound()
        track = Track(
            title=(info.get('title') or video_id)[:TITLE_MAX_LENGTH],
            thumbnail=info.get('thumbnail'),
            in_youtube=True,
            upload_by=request.user,
        )
        track.file.name = track_path(info['id'])
        track.save()
        return Response(TrackSerializer(track, context={'request': request}).data,
                        status=status.HTTP_201_CREATED)
