from rest_framework import serializers

from homepage.models import *


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


class HomePageSerializer(serializers.ModelSerializer):
    screens = ScreenSerializer(many=True, queryset=Screen.objects.all())
    photos = PhotoSerializer(many=True, queryset=Photo.objects.all())
    timeline_events = TimeLineEventSerializer(many=True, queryset=TimeLineEvent.objects.all())
    prizes = PrizeSerializer(many=True, queryset=Prize.objects.all())
    sponsors = SponsorSerializer(many=True, queryset=Sponsor.objects.all())
    organizations = OrganizationSerializer(many=True, queryset=Organization.objects.all())

    class Meta:
        model = Homepage
        fields = ['title_en', 'title_fa', 'screens', 'photos', 'timeline_events', 'prizes', 'sponsors', 'organizations']
