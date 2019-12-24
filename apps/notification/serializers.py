from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from apps.notification.models import Notification, Subscriber


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class SubscriberSerializer(ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=Subscriber.objects.all())])

    class Meta:
        model = Subscriber
        fields = "__all__"
