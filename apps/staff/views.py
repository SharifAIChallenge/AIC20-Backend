import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.staff.services.staffs_list_serializer import StaffsListSerializer
from . import serializers as staff_serializers
from . import models as staff_models


# Create your views here.


class StaffsListAPIView(GenericAPIView):
    queryset = staff_models.Staff.objects.all()

    def get(self, request):
        data = StaffsListSerializer(self.get_queryset()).data()
        return JsonResponse(data=data, status=status.HTTP_200_OK)
