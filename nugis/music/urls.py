from rest_framework.routers import DefaultRouter
from .views import (AlbumViewSet,
                    GenreViewSet,
                    TrackViewSet,
                    ArtisViewSet,
                    )


router = DefaultRouter()
router.register('albums', AlbumViewSet)
router.register('genres', GenreViewSet)
router.register('tracks', TrackViewSet)
router.register('artists', ArtisViewSet)

urlpatterns = router.urls
