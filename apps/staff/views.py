import json

from django.shortcuts import get_object_or_404
from rest_framework import status

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.staff.services.staffs_list_serializer import StaffsListSerializer
from . import serializers as staff_serializers
from . import models as staff_models


# Create your views here.


class StaffsListAPIView(GenericAPIView):

    def get(self, request):
        data = StaffsListSerializer().data()
        return Response(data={'staffs': json.dumps(data)}, status=status.HTTP_200_OK)
