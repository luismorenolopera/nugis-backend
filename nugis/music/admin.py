from django.contrib import admin
from .models import (Album,
                     Gender,
                     Artist,
                     Track,
                     TrackArtist,
                     TrackGender,
                     PlayList,
                     PlayListTrack)


admin.site.register(Album)
admin.site.register(Gender)
admin.site.register(Artist)
admin.site.register(Track)
admin.site.register(TrackArtist)
admin.site.register(TrackGender)
admin.site.register(PlayList)
admin.site.register(PlayListTrack)
