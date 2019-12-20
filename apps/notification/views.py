from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from apps.notification.models import Notification
from apps.notification.serializers import NotificationSerializer


@permission_classes([IsAuthenticated])
class NotificationView(GenericAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get(self, request):
        data = self.get_serializer(self.get_queryset().filter(user=request.user)).data
        return Response(data, status=status.HTTP_200_OK)
