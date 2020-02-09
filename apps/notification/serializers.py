from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from apps.notification.models import Notification, Subscriber


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        exclude = ['for_all']


class PublicNotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        exclude = ['for_all', 'user']


class SubscriberSerializer(ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=Subscriber.objects.all())])

    class Meta:
        model = Subscriber
        fields = "__all__"
