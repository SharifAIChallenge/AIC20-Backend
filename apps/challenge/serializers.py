from rest_framework.serializers import ModelSerializer

from . import models as challenge_models


class ChallengeSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Challenge
        fields = ['id', 'name', 'type', 'start_time', 'end_time']


class TournamentSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Tournament
        fields = ['id', 'type', 'start_time', 'end_time', 'run_time']


class StageSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Stage
        fields = ['id', 'finished']


class GroupSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Group
        fields = ['id']


class TeamGroupSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.TeamGroup
        fields = ['id']


class MatchSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Match
        fields = ['id', 'type']


class MatchTeamSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.MatchTeam
        fields = ['id']


class GameSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Game
        fields = ['id']


class GameSideSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.GameSide
        fields = ['id', 'has_won']


class GameTeamSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.GameTeam
        fields = ['id']


class InfoSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Info
        fields = ['id', 'status', 'detail']


class SubmissionSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Submission
        fields = ['id', 'type', 'submit_date']


class MapSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Map
        fields = ['__all__']
