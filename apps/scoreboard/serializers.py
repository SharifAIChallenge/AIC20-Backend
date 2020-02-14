from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from . import models as scoreboard_models
from ..participation import models as participation_models
from ..accounts import models as account_models


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = account_models.Profile
        fields = ['firstname_fa', 'lastname_fa']


class UserSerializer(ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['profile']


class ParticipantSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = participation_models.Participant
        fields = ['user']


class TeamSerializer(ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = participation_models.Team
        fields = ['name', 'participants', 'image']


class RowSerializer(ModelSerializer):
    team = TeamSerializer(read_only=True)

    class Meta:
        model = scoreboard_models.Row
        fields = ['team', 'score', 'wins', 'loss', 'rank']


class ScoreBoardSerializer(ModelSerializer):
    rows = RowSerializer(many=True, read_only=True)

    class Meta:
        model = scoreboard_models.ScoreBoard
        fields = ['rows', 'freeze']
