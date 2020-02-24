from rest_framework.serializers import ModelSerializer

from . import models as staff_models


class StaffSerializer(ModelSerializer):
    class Meta:
        model = staff_models.Staff
        fields = ['group_title', 'team_title', 'first_name_en', 'first_name_fa', 'last_name_en', 'last_name_fa', 'url',
                  'image', 'role']
