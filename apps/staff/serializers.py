from rest_framework.serializers import ModelSerializer

from . import models as staff_models


class StaffSerializer(ModelSerializer):
    class Meta:
        fields = ['__all__']
