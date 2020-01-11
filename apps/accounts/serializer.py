from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


from apps.accounts.models import Profile, ResetPasswordToken


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['user']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

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

    old_password = serializers.CharField(style={'input_type': 'password'})
    new_password1 = serializers.CharField(style={'input_type': 'password'})
    new_password2 = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['profile', 'email', 'old_password', 'new_password1', 'new_password2']

    def validate(self, data):
        if 'old_password' in data and 'new_password1' in data and 'new_password2' in data:
            if data['new_password1'] != data['new_password2']:
                raise serializers.ValidationError('passwords don\'t match!')
        elif 'old_password' in data or 'new_password1' in data or 'new_password2' in data:
            raise serializers.ValidationError('3 password fields required!')
        return data

    def update(self, instance, validated_data):
        if 'old_password' in validated_data:
            made_old_password = make_password(validated_data['old_password'])
            if instance.password != made_old_password:
                return
            instance.password = make_password(validated_data['new_password1'])
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


class ResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()


class ResetPasswordConfirmSerializer(serializers.ModelSerializer):

    new_password1 = serializers.CharField(max_length=100)
    new_password2 = serializers.CharField(max_length=100)

    class Meta:
        model = ResetPasswordToken
        fields = ['new_password1', 'new_password2', 'uid', 'token']

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError('passwords don\'t match!')
        return data
