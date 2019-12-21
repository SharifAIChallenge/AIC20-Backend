from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.notification.models import Notification, Subscriber


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class SubscriberSerializer(ModelSerializer):
    class Meta:
        model = Subscriber
        fields = "__all__"

    def validate(self, attrs):
        if Subscriber.objects.all().filter(email=attrs['email']):
            raise serializers.ValidationError('This email is already a subscriber')
        return attrs
