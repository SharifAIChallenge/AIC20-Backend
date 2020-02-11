from django.conf import settings
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from . import models as challenge_models
from ..participation import serializers as participation_serializers


class InfoSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Info
        fields = ['status', 'detail']


class GameTeamSerializer(ModelSerializer):
    team = participation_serializers.TeamSerializer(many=True, read_only=True)

    class Meta:
        model = challenge_models.GameTeam
        fields = ['game_side_id', 'team']


class GameSideSerializer(ModelSerializer):
    game_teams = GameTeamSerializer(many=True, read_only=True)

    class Meta:
        model = challenge_models.GameSide
        fields = ['game_id', 'has_won', 'game_teams']


class GameSerializer(ModelSerializer):
    info = InfoSerializer(read_only=True, allow_null=True)
    game_sides = GameSideSerializer(many=True, read_only=True)

    class Meta:
        model = challenge_models.Game
        fields = ['match_id', 'info', 'game_sides']


class MatchTeamSerializer(ModelSerializer):
    team = participation_serializers.TeamSerializer()

    class Meta:
        model = challenge_models.MatchTeam
        fields = ['match_id', 'team']


class MatchSerializer(ModelSerializer):
    match_teams = MatchTeamSerializer(many=True, read_only=True)
    games = GameSerializer(many=True, read_only=True)

    class Meta:
        model = challenge_models.Match
        fields = ['group_id', 'type', 'match_teams', 'games']


class TeamGroupSerializer(ModelSerializer):
    team = participation_serializers.TeamSerializer(read_only=True)

    class Meta:
        model = challenge_models.TeamGroup
        fields = ['group_id', 'team']


class GroupSerializer(ModelSerializer):
    team_groups = TeamGroupSerializer(many=True, read_only=True)
    matches = MatchSerializer(many=True, read_only=True)

    class Meta:
        model = challenge_models.Group
        fields = ['stage_id', 'team_groups', 'matches']


class StageSerializer(ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = challenge_models.Stage
        fields = ['tournament_id', 'finished', 'groups']


class TournamentSerializer(ModelSerializer):
    stages = StageSerializer(many=True, read_only=True)

    class Meta:
        model = challenge_models.Tournament
        fields = ['challenge_id', 'type', 'start_time', 'end_time', 'run_time', 'stages']


class ChallengeSerializer(ModelSerializer):
    tournaments = TournamentSerializer(many=True, read_only=True)

    class Meta:
        model = challenge_models.Challenge
        fields = ['name', 'type', 'start_time', 'end_time', 'tournaments']


class SubmissionSerializer(ModelSerializer):
    team = participation_serializers.TeamSerializer(read_only=True)
    user = participation_serializers.UserSerializer(read_only=True)

    class Meta:
        model = challenge_models.Submission
        fields = ['language', 'is_final', 'submit_time', 'team', 'user', 'file']


class SubmissionPostSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Submission
        fields = ['language', 'file']

    def validate(self, attrs):
        user = self.context['request'].user
        if not settings.ENABLE_SUBMISSION:
            raise serializers.ValidationError('Submission is closes')
        if not hasattr(user, 'participant'):
            raise serializers.ValidationError('You cant submit, because you dont have a team')
        attrs['user'] = user
        attrs['team'] = user.participant.team
        if attrs['file'].size > challenge_models.Submission.FILE_SIZE_LIMIT:
            raise serializers.ValidationError('File size limit exceeded')
        return attrs


class MapSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Map
        fields = ['name', 'infra_token']
