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
    def validate_file(self, value):
        if value.content_type != 'audio/mp3':
            raise serializers.ValidationError('file type not allowed')
        return value

    class Meta:
        model = Track
        fields = '__all__'
        read_only_fields = ('duration',)
        depth = 1



class GenreSerialializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class GenreDetailSerialializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'name', 'tracks')
        depth = 2
