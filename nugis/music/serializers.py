from rest_framework import serializers
from .models import (Album,
                     Genre,
                     Track,
                     )


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'
        read_only_fields = ('duration',)


class GenreSerialializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class GenreDetailSerialializer(serializers.ModelSerializer):
    tracks = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ('id', 'name', 'tracks')


    def get_tracks(self, obj):
        request = self.context.get('request')
        query = obj.tracks.all()
        return TrackSerializer(query,
                               many=True,
                               context={'request': request}
                               ).data
