from rest_framework.routers import DefaultRouter
from .views import AlbumViewSet


router = DefaultRouter()
router.register('albums', AlbumViewSet)

urlpatterns = router.urls
