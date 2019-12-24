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


class UserViewSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.save()
        profile = instance.profile
        profile.firstname_fa = validated_data.get('firstname_fa', profile.firstname_fa)
        profile.firstname_en = validated_data.get('firstname_en', profile.firstname_en)
        profile.lastname_fa = validated_data.get('lastname_fa', profile.lastname_fa)
        profile.lastname_en = validated_data.get('lastname_en', profile.lastname_en)
        profile.birth_date = validated_data.get('birth_date', profile.birth_date)
        profile.university = validated_data.get('university', profile.university)
        profile.save()
        return instance
