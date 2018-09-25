from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
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


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerialializer
    filter_backends = [SearchFilter,]
    search_fields = ['name']


    def retrieve(self, request, pk):
        query = get_object_or_404(Genre,
                                  pk=pk)
        serializer = GenreDetailSerialializer(query,
                                               context={'request': request})
        return Response(serializer.data)


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.order_by('-upload_date')
    serializer_class = TrackSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']
