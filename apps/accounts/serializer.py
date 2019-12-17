from django.contrib.auth.models import User
from rest_framework import serializers
from apps.translation.serializer import TranslatedTextSerializer
from apps.translation.models import TranslatedText
from apps.accounts.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    first_name = TranslatedTextSerializer()
    last_name = TranslatedTextSerializer()

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'birth_date', 'residence', 'education']

    def create(self, validated_data):
        first_name_data = validated_data.pop('first_name')
        last_name_data = validated_data.pop('last_name')
        profile = Profile.objects.create(**validated_data)
        TranslatedText.objects.create(profile=profile, **first_name_data)
        TranslatedText.objects.create(profile=profile, **last_name_data)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'password', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.get_or_create(user=user, **profile_data)
        return user


class ProfileTranslateSerializer(serializers.ModelSerializer):
    first_name_value = TranslatedTextSerializer()
    last_name_value = serializers.CharField()

    class Meta:
        model = Profile
        exclude = ['user', 'first_name', 'last_name']
