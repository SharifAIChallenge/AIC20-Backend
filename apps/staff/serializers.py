from rest_framework.serializers import ModelSerializer

from . import models as staff_models


class StaffSerializer(ModelSerializer):
    class Meta:
        model = staff_models.Staff
        fields = '__all__'

