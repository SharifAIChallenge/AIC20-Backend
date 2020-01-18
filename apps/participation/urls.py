from .views import BadgeViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('badge', BadgeViewSet)
urlpatterns = router.urls
