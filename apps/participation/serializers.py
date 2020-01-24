from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Badge, Team, Participant, Invitation
from ..accounts import serializer as accounts_serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Participant
        fields = ['id', 'user']


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['id', 'title', 'text', 'image']


class TeamSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)
    badges = BadgeSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'badges', 'participants']


class InvitationSerializer(serializers.ModelSerializer):
    target = accounts_serializers.UserSerializer()
    source = accounts_serializers.UserSerializer()

    class Meta:
        model = Invitation
        fields = ['target', 'source']
