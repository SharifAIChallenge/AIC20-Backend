from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name']

    def validate(self, attrs):
        if len(attrs['password']) < 4:
            return serializers.ValidationError('password is too short')
        return attrs
