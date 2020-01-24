from rest_framework import viewsets
from .serializers import BadgeSerializer, ParticipantSerializer
from .models import Badge, Participant

class BadgeViewSet(viewsets.ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
