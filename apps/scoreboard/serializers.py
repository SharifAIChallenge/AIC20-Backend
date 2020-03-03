from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

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