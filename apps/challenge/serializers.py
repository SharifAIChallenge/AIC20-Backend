from datetime import datetime, timedelta

from django.conf import settings
from django.utils.timezone import utc
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.challenge.models import SubmissionStatusTypes, ChallengeTypes
from apps.participation.serializers import LimitedTeamSerializer
from . import models as challenge_models
from ..participation import serializers as participation_serializers


class GameTeamSerializer(ModelSerializer):
    team = participation_serializers.GameLimitedTeamSerializer(read_only=True)

    class Meta:
        model = challenge_models.GameTeam
        fields = ['team', 'log', 'score']

    # def to_representation(self, instance: challenge_models.GameTeam):
    #     data = super().to_representation(instance)
    #     if hasattr(self.context['request'].user, 'participant') and self.context[
    #         'request'].user.participant.team_id != instance.team_id:
    #         data['log'] = None
    #     return data


class GameSideSerializer(ModelSerializer):
    game_teams = GameTeamSerializer(many=True, read_only=True)

    class Meta:
        model = challenge_models.GameSide
        fields = ['has_won', 'game_teams']


class GameSerializer(ModelSerializer):
    game_sides = GameSideSerializer(many=True, read_only=True)
    tournament = serializers.SerializerMethodField('_get_tournament')

    @staticmethod
    def _get_tournament(instance: challenge_models.Game):
        if instance.game_sides.last().game_teams.last().team.challenge.type == ChallengeTypes.FINAL:
            return 'final'
        return 'friendly' if instance.match == None else instance.match.group.stage.tournament.name

    class Meta:
        model = challenge_models.Game
        fields = ['tournament', 'match', 'infra_game_message', 'game_sides', 'status', 'time', 'log']


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
        model = challenge_models.GroupTeam
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
    class Meta:
        model = challenge_models.Tournament
        fields = ['name', 'type', 'start_time', 'end_time']


class ChallengeSerializer(ModelSerializer):
    tournaments = TournamentSerializer(many=True, read_only=True)

    class Meta:
        model = challenge_models.Challenge
        fields = ['name', 'type', 'start_time', 'end_time', 'tournaments', 'friendly_game_delay', 'code_submit_delay',
                  'can_submit', 'can_change_submission']


class SubmissionSerializer(ModelSerializer):
    user = participation_serializers.UserSerializer(read_only=True)

    class Meta:
        model = challenge_models.Submission
        fields = ['id', 'language', 'is_final', 'submit_time', 'user', 'file', 'download_link', 'status']


class SubmissionPostSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Submission
        fields = ['language', 'file']

    def validate(self, attrs):
        user = self.context['request'].user

        if not hasattr(user, 'participant'):
            raise serializers.ValidationError('You cant submit, because you dont have a team')
        attrs['user'] = user
        attrs['team'] = user.participant.team
        if attrs['file'].size > challenge_models.Submission.FILE_SIZE_LIMIT:
            raise serializers.ValidationError('File size limit exceeded')
        if not attrs['team'].is_valid:
            raise serializers.ValidationError('Please complete your team first')
        submissions = attrs['team'].submissions
        challenge = challenge_models.Challenge.objects.get(type=challenge_models.ChallengeTypes.FINAL)
        if not challenge.can_submit:
            raise serializers.ValidationError('Submission is closed')

        if submissions.exists() and datetime.now(utc) - submissions.order_by('-submit_time')[0].submit_time < timedelta(
                minutes=challenge.code_submit_delay):
            raise serializers.ValidationError(
                f"You have to wait at least {settings.TEAM_SUBMISSION_TIME_DELTA} minute between each submission!")

        return attrs

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.handle()
        return instance


class SubmissionSecondMethodPostSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Submission
        fields = ['language', 'infra_token', 'download_link']

    def validate(self, attrs):
        user = self.context['request'].user

        if not hasattr(user, 'participant'):
            raise serializers.ValidationError('You cant submit, because you dont have a team')
        attrs['user'] = user
        attrs['team'] = user.participant.team
        attrs['status'] = SubmissionStatusTypes.UPLOADED
        if not attrs['team'].is_valid:
            raise serializers.ValidationError('Please complete your team first')
        submissions = attrs['team'].submissions
        challenge = challenge_models.Challenge.objects.get(type=challenge_models.ChallengeTypes.FINAL)
        if not challenge.can_submit:
            raise serializers.ValidationError('Submission is closed')

        if submissions.exists() and datetime.now(utc) - submissions.order_by('-submit_time')[0].submit_time < timedelta(
                minutes=challenge.code_submit_delay):
            raise serializers.ValidationError(
                f"You have to wait at least {settings.TEAM_SUBMISSION_TIME_DELTA} minute between each submission!")

        return attrs

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.handle()
        return instance


class MapSerializer(ModelSerializer):
    class Meta:
        model = challenge_models.Map
        fields = ['name', 'infra_token']


class LobbySerializer(ModelSerializer):
    teams1 = LimitedTeamSerializer(many=True)
    teams2 = LimitedTeamSerializer(many=True)

    class Meta:
        model = challenge_models.Lobby
        fields = ['teams1', 'teams2', 'multi_play', 'with_friend']

    def to_representation(self, instance: challenge_models.Lobby):
        data = super().to_representation(instance)
        if instance.challenge.type == challenge_models.ChallengeTypes.FINAL:
            team1 = instance.teams1.all().first()
            team2 = instance.teams2.all().first()
            if team1:
                data['teams1'] = [LimitedTeamSerializer(team1).data, LimitedTeamSerializer(team1).data]
            if team2:
                data['teams2'] = [LimitedTeamSerializer(team2).data, LimitedTeamSerializer(team2).data]
        return data
