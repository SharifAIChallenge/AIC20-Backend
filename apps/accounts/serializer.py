from django.contrib.auth.models import User
from rest_framework import serializers

from apps.accounts.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['user']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'password', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user


class ProfileTranslateSerializer(serializers.ModelSerializer):
    first_name_value = serializers.CharField()
    last_name_value = serializers.CharField()

    class Meta:
        model = Profile
        exclude = ['user', 'first_name_fa', 'first_name_en', 'last_name_fa', 'last_name_en']
