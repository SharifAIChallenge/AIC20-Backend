from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from apps.accounts.models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        exclude = ['user']


class UserSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer()

    password_1 = serializers.CharField(style={'input_type': 'password'})
    password_2 = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password_1', 'password_2', 'profile']

    def validate(self, data):
        if data['password_1'] != data['password_2']:
            raise serializers.ValidationError('passwords don\'t match!')
        return data

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        validated_data.pop('password_1')
        validated_data['password'] = make_password(validated_data.pop('password_2'))
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user

