from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from apps.accounts.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'password', 'email', 'first_name']

    def validate(self, attrs):
        if len(attrs['password']) < 4:
            raise serializers.ValidationError('password is too short')
        return attrs

    def validate_password(self, value: str) -> str:
        return make_password(value)
