from rest_framework import serializers
from .models import (Album,
                     Genre,
                     Track,
                     Artist,
                     PlayList,
                     )


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'


class TrackSerializer(serializers.ModelSerializer):
    upload_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate_file(self, value):
        if value.content_type != 'audio/mp3':
            raise serializers.ValidationError('file type not allowed')
        return value

    class Meta:
        model = Track
        fields = ('id',
                  'file',
                  'title',
                  'duration',
                  'in_youtube',
                  'thumbnail',
                  'upload_date',
                  'upload_by',
                  'album',
                  'artists',
                  'genders')
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


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'


class ArtistDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'alias', 'first_name', 'last_name', 'tracks')
        depth = 2


class PlayListSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = PlayList
        fields = ('id', 'name', 'owner', 'tracks')
        depth = 2


class YoutubeSetSerializer(serializers.Serializer):
    id = serializers.CharField(help_text='id from a youtube video')


class PlayListTrackSerializer(serializers.Serializer):
    playlist = serializers.PrimaryKeyRelatedField(read_only=True)


class PlaylistTrackSerializerBody(serializers.Serializer):
    track = serializers.IntegerField(help_text='id of a track')
    playlists = serializers.ListField(
        help_text='list of ids',
        child=serializers.IntegerField()
    )
