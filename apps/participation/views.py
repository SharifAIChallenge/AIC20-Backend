from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from . import models as participation_models
from . import serializers as participation_serializers


class BadgeListAPIView(GenericAPIView):
    queryset = participation_models.Badge.objects.all()
    serializer_class = participation_serializers.BadgeSerializer

    def get(self, request):
        data = self.get_serializer(self.get_queryset(), many=True).data
        return Response(data={'badges': data}, status=status.HTTP_200_OK)


class ParticipantListAPIView(GenericAPIView):
    queryset = participation_models.Participant.objects.all()
    serializer_class = participation_serializers.ParticipantSerializer

    def get(self, request):
        data = self.get_serializer(self.get_queryset(), many=True).data
        return Response(data={'participants': data}, status=status.HTTP_200_OK)
