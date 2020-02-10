import os

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
    is_valid = serializers.SerializerMethodField('_is_valid', read_only=True)

    @staticmethod
    def _is_valid(team: Team):
        return team.is_valid

    class Meta:
        model = Team
        fields = ['name', 'badges', 'participants', 'image', 'is_valid']


class TeamPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'image']

    def validate(self, attrs):
        image = attrs.get('image')
        if image and os.path.splitext(image.name[1][1:]) not in Team.VALID_IMAGE_FORMATS:
            raise serializers.ValidationError('Invalid file format')
        if image and image.size > Team.IMAGE_MAX_SIZE:
            raise serializers.ValidationError('Maximum file size reached')
        return attrs


class InvitationSerializer(serializers.ModelSerializer):
    target = UserSerializer()
    source = UserSerializer()
    team_name = serializers.SerializerMethodField('_team_name', read_only=True)

    @staticmethod
    def _team_name(invitation: Invitation):
        return invitation.source.participant.team.name

    class Meta:
        model = Invitation
        fields = ['id', 'target', 'source', 'team_name', 'status']
