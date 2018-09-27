from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
import youtube_dl
from .models import Track
from .serializers import TrackSerializer
import linecache
import sys

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))




OPTIONS = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
    }],
    'outtmpl': settings.BASE_DIR + '/media/documents/music' + '/%(id)s.%(ext)s',
}


def extract_data_video(url):
    try:
        with youtube_dl.YoutubeDL(OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'id': info['id'],
                'url': info['webpage_url'],
                'title': info['title'],
                'thumbnail': info['thumbnail']
                }
    except Exception as e:
        raise NotFound()


def download_video(url, user):
    filePath = 'documents/music/{0}.mp3'.format(url.split('watch?v=')[1])
    if Track.objects.filter(file_data=filePath).exists():
        raise ValidationError({'detail': 'track exist'})
    try:
        with youtube_dl.YoutubeDL(OPTIONS) as ydl:
            info = ydl.extract_info(url, download=True)

        track = Track.objects.create(
            title=info['title'],
            thumbnail=info['thumbnail'],
            upload_by=user
        )
        track.file_data.name = 'documents/music/{0}.mp3'.format(info['id'])
        track.save()
        serializer = TrackSerializer(track)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)
    except:
        PrintException()
        raise NotFound()
