from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from . import models as scoreboard_models
from ..participation import models as participation_models
from ..accounts import models as account_models


class TeamSerializer(ModelSerializer):
    class Meta:
        model = participation_models.Team
        fields = ['name', 'image']


class RowSerializer(ModelSerializer):
    team = TeamSerializer(read_only=True)

    class Meta:
        model = scoreboard_models.Row
        fields = ['team', 'score', 'wins', 'loss', 'draws']


class GroupScoreBoardSerializer(ModelSerializer):
    group_name = SerializerMethodField('_group_name')

    @staticmethod
    def _group_name(instance: scoreboard_models.GroupScoreBoard):
        return instance.group.name

    class Meta:
        model = scoreboard_models.GroupScoreBoard
        fields = ['group_name']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['rows'] = RowSerializer(instance.rows.all().order_by('-score'), many=True).data
        return data
