from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from requests import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from apps.notification.models import Notification
from apps.notification.serializers import NotificationSerializer


class NotificationView(GenericAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get(self, request):
        data = self.get_serializer(self.get_queryset().filter(request.user.is_authenticated)).data
        return Response(data, status=status.HTTP_200_OK)
