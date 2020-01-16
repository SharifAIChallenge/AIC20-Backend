from rest_framework.serializers import ModelSerializer

from . import models as challenge_models


class ChallengeSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Challenge
        fields = ['__all__']


class TournamentSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Tournament
        fields = ['__all__']


class StageSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Stage
        fields = ['__all__']


class GroupSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Group
        fields = ['__all__']


class TeamGroupSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.TeamGroup
        fields = ['__all__']


class MatchSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Match
        fields = ['__all__']


class MatchTeamSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.MatchTeam
        fields = ['__all__']


class GameSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Game
        fields = ['__all__']


class GameSideSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.GameSide
        fields = ['__all__']


class GameTeamSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.GameTeam
        fields = ['__all__']


class InfoSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Info
        fields = ['__all__']


class SubmissionSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Submission
        fields = ['__all__']


class MapSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Map
        fields = ['__all__']
