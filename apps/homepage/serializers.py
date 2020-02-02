from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from .models import Intro, TimelineEvent, Prize, Stat, Sponsor, WhyThisEvent, Quote


class IntroSerializer(ModelSerializer):
    class Meta:
        model = Intro
        fields = '__all__'


class TimelineEventSerializer(ModelSerializer):
    class Meta:
        model = TimelineEvent
        fields = '__all__'


class PrizeSerializer(ModelSerializer):
    class Meta:
        model = Prize
        fields = '__all__'


class StatSerializer(ModelSerializer):
    class Meta:
        model = Stat
        fields = '__all__'


class SponsorSerializer(ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'


class WhyThisEventSerializer(ModelSerializer):
    class Meta:
        model = WhyThisEvent
        fields = '__all__'


class QuoteSerializer(ModelSerializer):
    class Meta:
        model = Quote
        fields = '__all__'
