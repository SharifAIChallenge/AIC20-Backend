from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.accounts.serializer import ProfileSerializer
from apps.challenge.models import Challenge
from .models import Badge, Team, Participant, Invitation
from ..accounts import serializer as accounts_serializers


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'profile']


class ParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Participant
        fields = ['user']


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['title', 'text', 'image']


class TeamSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)
    badges = BadgeSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ['name', 'badges', 'participants', 'image']


class TeamPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'image']


class InvitationSerializer(serializers.ModelSerializer):
    target = UserSerializer()
    source = UserSerializer()
    team_name = serializers.SerializerMethodField('_team_name', read_only=True)

    @staticmethod
    def _team_name(invitation: Invitation):
        return invitation.source.participant.team.name

    class Meta:
        model = Invitation
        fields = ['target', 'source', 'team_name']
