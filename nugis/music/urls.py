from rest_framework.routers import DefaultRouter
from .views import (AlbumViewSet,
                    GenderViewSet,
                    TrackViewSet
                    )


router = DefaultRouter()
router.register('albums', AlbumViewSet)
router.register('genders', GenderViewSet)
router.register('tracks', TrackViewSet)

urlpatterns = router.urls
