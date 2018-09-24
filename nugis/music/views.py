from rest_framework import viewsets
from .models import Album
from .serializers import AlbumSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    """Doc for album view"""
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
