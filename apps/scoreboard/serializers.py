from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from apps.challenge.models import GameTeam
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


class ChallengeScoreBoardSerializer(ModelSerializer):
    challenge_type = SerializerMethodField('_challenge_type')

    @staticmethod
    def _challenge_type(instance: scoreboard_models.ChallengeScoreBoard):
        return instance.challenge.type

    class Meta:
        model = scoreboard_models.ChallengeScoreBoard
        fields = ['challenge_type']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        teams_with_game_ids = GameTeam.objects.distinct('team_id').values_list('team_id')
        data['rows'] = RowSerializer(instance.rows.all().order_by('-score').filter(team_id__in=teams_with_game_ids),
                                     many=True).data
        return data
