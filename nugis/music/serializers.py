from django.conf import settings
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

    # Browsers send audio/mpeg for .mp3; some old ones send audio/mp3.
    ALLOWED_TYPES = ('audio/mpeg', 'audio/mp3', 'audio/mpeg3', 'audio/x-mpeg-3')

    def validate_file(self, value):
        content_type = getattr(value, 'content_type', '')
        if content_type not in self.ALLOWED_TYPES:
            raise serializers.ValidationError('file type not allowed')
        if value.size > settings.MAX_TRACK_SIZE:
            raise serializers.ValidationError('file too large')
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
        read_only_fields = ('tracks',)
        depth = 2


class YoutubeSetSerializer(serializers.Serializer):
    id = serializers.RegexField(r'^[A-Za-z0-9_-]{11}$',
                                help_text='id from a youtube video')


class PlayListTrackSerializer(serializers.Serializer):
    playlist = serializers.PrimaryKeyRelatedField(read_only=True)


class PlaylistTrackSerializerBody(serializers.Serializer):
    track = serializers.IntegerField(help_text='id of a track')
    playlists = serializers.ListField(
        help_text='list of ids',
        child=serializers.IntegerField()
    )
