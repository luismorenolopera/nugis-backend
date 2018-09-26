from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (AlbumViewSet,
                    GenreViewSet,
                    TrackViewSet,
                    ArtistViewSet,
                    PlayListViewSet,
                    YouTubeTrackDownload,
                    )


router = DefaultRouter()
router.register('albums', AlbumViewSet)
router.register('genres', GenreViewSet)
router.register('tracks', TrackViewSet)
router.register('artists', ArtistViewSet)
router.register('playlists', PlayListViewSet)

urlpatterns = [
    path(
        'yt_upload',
        YouTubeTrackDownload.as_view()
    )
]

urlpatterns += router.urls
