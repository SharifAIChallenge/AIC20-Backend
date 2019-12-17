from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from .models import Document, Section, Subsection


class SubtitleSerializer(ModelSerializer):
    subtitle_value = serializers.CharField()

    class Meta:
        model = Subsection
        fields = ['subtitle_value']


class SectionSerializer(ModelSerializer):
    subtitles = SubtitleSerializer(many=True, read_only=True)
    title_value = serializers.CharField()

    class Meta:
        model = Section
        fields = ['uuid', 'title_value', 'markdown', 'subtitles']


class DocumentSerializer(ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)
    title_value = serializers.CharField()
    description_value = serializers.CharField()

    class Meta:
        model = Document
        fields = ['title_value', 'description_value', 'sections']
