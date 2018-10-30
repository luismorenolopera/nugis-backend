from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import (Album,
                     Genre,
                     Track,
                     Artist,
                     PlayList,
                     PlayListTrack,
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


class AlbumViewSet(ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    pagination_class = SortResultsSetPagination


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action != 'retrieve':
            return GenreSerialializer
        return GenreDetailSerialializer


class TrackViewSet(ModelViewSet):
    queryset = Track.objects.order_by('-upload_date')
    serializer_class = TrackSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_fields = ('upload_by',)
    search_fields = ('title',)
    pagination_class = SortResultsSetPagination


class ArtistViewSet(ModelViewSet):
    queryset = Artist.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['alias', 'first_name', 'last_name']
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action != 'retrieve':
            return ArtistSerializer
        return ArtistDetailSerializer


class PlayListViewSet(ModelViewSet):
    queryset = PlayList.objects.all()
    serializer_class = PlayListSerializer

    def get_queryset(self):
        user = self.request.user
        return PlayList.objects.filter(owner=user)


class TrackPlayListsView(APIView):
    def post(self, request):
        playlists_ids = request.data['playlists']
        track_id = request.data['track']
        track = Track.objects.get(pk=track_id)
        PlayListTrack.objects.filter(playlist__owner=request.user,
                                     track=track).delete()
        for playlist_id in playlists_ids:
            playlist = PlayList.objects.get(pk=playlist_id)
            PlayListTrack(playlist=playlist, track=track).save()
        return Response({'status': 'ok'})
