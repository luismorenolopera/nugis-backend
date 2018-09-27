from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from .models import (Album,
                     Genre,
                     Track,
                     Artist,
                     PlayList,
                     )
from .serializers import (AlbumSerializer,
                          GenreSerialializer,
                          GenreDetailSerialializer,
                          TrackSerializer,
                          ArtistSerializer,
                          ArtistDetailSerializer,
                          PlayListSerializer,
                          )
from nugis.pagination import (SortResultsSetPagination,
                              StandardResultsSetPagination,
                              )
from .yt import extract_data_video


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
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_fields = ('upload_by',)
    search_fields = ('title',)
    pagination_class = SortResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        return Track.objects.filter(upload_by=user).order_by('-upload_date')


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['alias', 'first_name', 'last_name']
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action != 'retrieve':
            return ArtistSerializer
        return ArtistDetailSerializer


class PlayListViewSet(viewsets.ModelViewSet):
    queryset = PlayList.objects.all()
    serializer_class = PlayListSerializer

    def get_queryset(self):
        user = self.request.user
        return PlayList.objects.filter(owner=user)


class YouTubeTrackDownload(APIView):
    def get(self, request, format=None):
        url = request.data['url']
        if len(url.split('list=')) > 1:
            raise ValidationError({'detail': 'playlist does not support.'})
        return Response(extract_data_video(url))

    def post(self, request, format=None):
        pass
