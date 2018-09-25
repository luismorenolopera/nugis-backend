from rest_framework.routers import DefaultRouter
from .views import (AlbumViewSet,
                    GenreViewSet,
                    TrackViewSet
                    )


router = DefaultRouter()
router.register('albums', AlbumViewSet)
router.register('genre', GenreViewSet)
router.register('tracks', TrackViewSet)

urlpatterns = router.urls
