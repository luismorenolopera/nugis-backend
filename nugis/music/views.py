from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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
                          PlayListTrackSerializer,
                          PlaylistTrackSerializerBody,
                          )
from .permissions import IsStaffOrReadOnly, IsUploaderOrReadOnly
from nugis.pagination import (SortResultsSetPagination,
                              StandardResultsSetPagination,
                              )


class AlbumViewSet(ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = (IsAuthenticated, IsStaffOrReadOnly)
    pagination_class = SortResultsSetPagination


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.order_by('name')
    permission_classes = (IsAuthenticated, IsStaffOrReadOnly)
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action != 'retrieve':
            return GenreSerialializer
        return GenreDetailSerialializer


class TrackViewSet(ModelViewSet):
    queryset = (Track.objects.order_by('-upload_date')
                .select_related('album', 'upload_by')
                .prefetch_related('artists', 'genders'))
    serializer_class = TrackSerializer
    permission_classes = (IsAuthenticated, IsUploaderOrReadOnly)
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ('upload_by',)
    search_fields = ('title',)
    pagination_class = SortResultsSetPagination


class ArtistViewSet(ModelViewSet):
    queryset = Artist.objects.order_by('alias', 'first_name')
    permission_classes = (IsAuthenticated, IsStaffOrReadOnly)
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
        return (PlayList.objects.filter(owner=self.request.user)
                .order_by('name')
                .prefetch_related('tracks__artists', 'tracks__genders',
                                  'tracks__album'))


class TrackPlayListsView(APIView):
    id_track_get = openapi.Parameter(
        'id',
        openapi.IN_QUERY,
        description='track id',
        type=openapi.TYPE_INTEGER
    )
    description_post = 'receives the id of a track and the list of id ' \
                       'from the playlists to which to belong'

    @swagger_auto_schema(manual_parameters=[id_track_get])
    def get(self, request):
        track = request.query_params.get('id')
        if not track or not str(track).isdigit():
            raise ValidationError({'detail': 'id is required'})
        playlists = PlayListTrack.objects.filter(playlist__owner=request.user,
                                                 track=track)
        serializer = PlayListTrackSerializer(playlists, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description=description_post,
                         request_body=PlaylistTrackSerializerBody,
                         responses={201: 'ok'})
    def post(self, request):
        body = PlaylistTrackSerializerBody(data=request.data)
        body.is_valid(raise_exception=True)
        track = get_object_or_404(Track, pk=body.validated_data['track'])
        ids = set(body.validated_data['playlists'])
        # Only the user's own playlists can be touched.
        playlists = list(PlayList.objects.filter(owner=request.user,
                                                 pk__in=ids))
        if len(playlists) != len(ids):
            raise ValidationError({'playlists': 'invalid playlist id'})
        PlayListTrack.objects.filter(playlist__owner=request.user,
                                     track=track).delete()
        PlayListTrack.objects.bulk_create(
            [PlayListTrack(playlist=p, track=track) for p in playlists]
        )
        return Response({'detail': 'ok'}, status=status.HTTP_201_CREATED)
