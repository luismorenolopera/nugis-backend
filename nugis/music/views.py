from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import (Album,
                     Genre,
                     Track,
                     )
from .serializers import (AlbumSerializer,
                          GenreSerialializer,
                          GenreDetailSerialializer,
                          TrackSerializer
                          )
from nugis.pagination import SortResultsSetPagination


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    pagination_class = SortResultsSetPagination


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GenreDetailSerialializer
        return GenreSerialializer


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.order_by('-upload_date')
    serializer_class = TrackSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']
    pagination_class = SortResultsSetPagination
