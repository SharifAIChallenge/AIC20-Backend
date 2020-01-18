from rest_framework import serializers
from .models import Badge, Team, Participant

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant

