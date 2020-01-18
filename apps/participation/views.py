from rest_framework import viewsets
from .serializers import BadgeSerializer
from .models import Badge

class BadgeViewSet(viewsets.ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
