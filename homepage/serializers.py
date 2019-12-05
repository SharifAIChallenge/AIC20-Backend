from rest_framework import serializers

from homepage.models import *


class HomePageSerializer(serializers.ModelSerializer):
    Photos = serializers.PrimaryKeyRelatedField(many=True, source='job_set', queryset=Photo.objects.all())

    class Meta:
        model = Homepage
        fields = ['title_en', 'title_fa']


class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'


class TimeLineEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLineEvent
        fields = '__all__'


class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        fields = '__all__'


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'