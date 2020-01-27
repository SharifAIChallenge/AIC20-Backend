from rest_framework.serializers import ModelSerializer

from . import models as challenge_models
from ..participation import serializers as participation_serializers


class InfoSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Info
        fields = ['id', 'status', 'detail']


class GameTeamSerializer(ModelSerializer):
    team = participation_serializers.TeamSerializer(many=True, read_only=True)

    class Meta:
        model = challenge_models.GameTeam
        fields = ['id', 'game_side_id', 'team']


class GameSideSerializer(ModelSerializer):
    game_teams = GameTeamSerializer(many=True, read_only=True)

    class Meta:
        model = challenge_models.GameSide
        fields = ['id', 'game_id', 'has_won', 'game_teams']


class GameSerializer(ModelSerializer):
    info = InfoSerializer(read_only=True, allow_null=True)
    game_sides = GameSideSerializer(many=True, read_only=True)

    class Meta:
        model = challenge_models.Game
        fields = ['id', 'match_id', 'info', 'game_sides']


class MatchTeamSerializer(ModelSerializer):
    team = participation_serializers.TeamSerializer()

    class Meta:
        model = challenge_models.MatchTeam
        fields = ['id', 'match_id', 'team']


class MatchSerializer(ModelSerializer):
    match_teams = MatchTeamSerializer(many=True, read_only=True)
    games = GameSerializer(many=True, read_only=True)

    class Meta:
        model = challenge_models.Match
        fields = ['id', 'group_id', 'type', 'match_teams', 'games']


class TeamGroupSerializer(ModelSerializer):
    team = participation_serializers.TeamSerializer(read_only=True)

    class Meta:
        model = challenge_models.TeamGroup
        fields = ['id', 'group_id', 'team']


class GroupSerializer(ModelSerializer):
    team_groups = TeamGroupSerializer(many=True, read_only=True)
    matches = MatchSerializer(many=True, read_only=True)

    class Meta:
        model = challenge_models.Group
        fields = ['id', 'stage_id', 'team_groups', 'matches']


class StageSerializer(ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = challenge_models.Stage
        fields = ['id', 'tournament_id', 'finished', 'groups']


class TournamentSerializer(ModelSerializer):
    stages = StageSerializer(many=True, read_only=True)

    class Meta:
        model = challenge_models.Tournament
        fields = ['id', 'challenge_id', 'type', 'start_time', 'end_time', 'run_time', 'stages']


class ChallengeSerializer(ModelSerializer):
    tournaments = TournamentSerializer(many=True, read_only=True)

    class Meta:
        model = challenge_models.Challenge
        fields = ['id', 'name', 'type', 'start_time', 'end_time', 'tournaments']


class SubmissionSerializer(ModelSerializer):
    team = participation_serializers.TeamSerializer(read_only=True)
    user = participation_serializers.UserSerializer(read_only=True)

    class Meta:
        model = challenge_models.Submission
        fields = ['id', 'language', 'is_final', 'submit_date', 'team', 'user']


class SubmissionPostSerializer(ModelSerializer):
    class Meta:
        fields = ['team_id', 'user_id', 'language', 'file']


class MapSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Map
        fields = ['id', 'name', 'infra_token']
