from django.contrib import admin
from .models import (Album,
                     Genre,
                     Artist,
                     Track,
                     TrackArtist,
                     TrackGenre,
                     PlayList,
                     PlayListTrack)


admin.site.register(Album)
admin.site.register(Genre)
admin.site.register(Artist)
admin.site.register(Track)
admin.site.register(TrackArtist)
admin.site.register(TrackGenre)
admin.site.register(PlayList)
admin.site.register(PlayListTrack)
