from .views import BadgeViewSet, ParticipantViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('badge', BadgeViewSet)
router.register('participant', ParticipantViewSet)
urlpatterns = router.urls
