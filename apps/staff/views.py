from django.shortcuts import get_object_or_404
from rest_framework import status

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from . import serializers as staff_serializers
from . import models as staff_models


# Create your views here.


class StaffsListAPIView(GenericAPIView):
    queryset = staff_models.Staff.objects.all()
    serializer_class = staff_serializers.StaffSerializer

    def get(self, request):
        data = self.get_serializer(self.get_queryset(), many=True).data
        return Response(data={'staffs': data}, status=status.HTTP_200_OK)


g


class StaffsByTitleListAPIView(GenericAPIView):
    queryset = staff_models.Staff.objects.all()
    serializer_class = staff_serializers.StaffSerializer

    def get(self, request, title):
        data = self.get_serializer(self.get_queryset().filter(title=title), many=True).data
        return Response(data={'staffs': data}, status=status.HTTP_200_OK)
