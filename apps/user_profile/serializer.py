from rest_framework import serializers

from apps.user_profile.models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'password', 'email', 'first_name']

    def validate(self, attrs):
        if len(attrs['password']) < 4:
            return serializers.ValidationError('password is too short')
        return attrs
