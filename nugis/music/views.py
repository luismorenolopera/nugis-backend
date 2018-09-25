from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from .models import (Album,
                     Gender,
                     Track,
                     )
from .serializers import (AlbumSerializer,
                          GenderSerialializer,
                          GenderDetailSerialializer,
                          TrackSerializer
                          )


class AlbumViewSet(viewsets.ModelViewSet):
    """Doc for album view"""
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer



class GenderViewSet(viewsets.ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerialializer
    filter_backends = [SearchFilter,]
    search_fields = ['name']


    def retrieve(self, request, pk):
        query = get_object_or_404(Gender,
                                  pk=pk)
        serializer = GenderDetailSerialializer(query,
                                               context={'request': request})
        return Response(serializer.data)


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
