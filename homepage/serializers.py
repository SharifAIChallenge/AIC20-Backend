from rest_framework import serializers
from rest_framework.utils import json

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
        model = Organizer
        fields = '__all__'


class HomePageSerializer(serializers.ModelSerializer):
    dictionary = serializers.SerializerMethodField('get_dict')

    def get_dict(self, a):
        serializer_dictionary = dict()
        serializer_dictionary['screens'] = ScreenSerializer(Screen.objects.all(), many=True).data
        serializer_dictionary['photos'] = PhotoSerializer(Photo.objects.all(), many=True).data
        serializer_dictionary['timeline_events'] = TimeLineEventSerializer(TimeLineEvent.objects.all(), many=True).data
        serializer_dictionary['prizes'] = PrizeSerializer(Prize.objects.all(), many=True).data
        serializer_dictionary['sponsors'] = SponsorSerializer(Sponsor.objects.all(), many=True).data
        serializer_dictionary['organizations'] = OrganizationSerializer(Organizer.objects.all(), many=True).data

        dictionary = json.dumps(serializer_dictionary)
        return dictionary

    class Meta:
        model = Homepage
        fields = ('title_en', 'title_fa', 'dictionary')
