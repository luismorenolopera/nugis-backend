from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import (Album,
                     Genre,
                     Track,
                     Artist
                     )
from .serializers import (AlbumSerializer,
                          GenreSerialializer,
                          GenreDetailSerialializer,
                          TrackSerializer,
                          ArtistSerializer,
                          ArtistDetailSerializer,
                          )
from nugis.pagination import (SortResultsSetPagination,
                              StandardResultsSetPagination,
                              )


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    pagination_class = SortResultsSetPagination


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action != 'retrieve':
            return GenreSerialializer
        return GenreDetailSerialializer


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.order_by('-upload_date')
    serializer_class = TrackSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']
    pagination_class = SortResultsSetPagination


class ArtisViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['alias', 'first_name', 'last_name']
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action != 'retrieve':
            return ArtistSerializer
        return ArtistDetailSerializer
