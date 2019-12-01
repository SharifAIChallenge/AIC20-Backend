from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from .models import Document, Section, Subtitle


class SubtitleSerializer(ModelSerializer):
    class Meta:
        model = Subtitle
        fields = ['subtitle']

    def validate(self, attrs):
        if 'subtitle' not in attrs:
            raise serializers.ValidationError('Subtitle Field Missing!')
        if not attrs['subtitle']:
            raise serializers.ValidationError('Subtitle Field is Empty')
        if len(attrs) > 1:
            raise serializers.ValidationError('Too Many Fields')
        return attrs


class SectionSerializer(ModelSerializer):
    """
        Main Serializer fo Section Model
    """
    subtitles = SubtitleSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ['title', 'markdown', 'subtitles']

    def validate(self, attrs):
        if 'title' not in attrs:
            raise serializers.ValidationError('Title Field Missing!')
        if 'markdown' not in attrs:
            raise serializers.ValidationError('Markdown Field Missing!')
        if not attrs['title']:
            raise serializers.ValidationError('Title Field is Empty')
        if not attrs['markdown']:
            raise serializers.ValidationError('Markdown Field is Empty')

        if len(attrs) > 2:
            raise serializers.ValidationError('Too Many Fields')
        return attrs


class SectionSerializerForAPIVIewOfASpecificDocument(ModelSerializer):
    subtitles = SubtitleSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ['title', 'uuid', 'subtitles']


class SectionSerializerForDocument(ModelSerializer):
    """
        This Serializer is only for getting Documents, serialized Data
    """
    subtitles = SubtitleSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ['title', 'subtitles']


class DocumentSerializer(ModelSerializer):
    sections = SectionSerializerForDocument(many=True, read_only=True)

    class Meta:
        model = Document
        fields = ['title', 'sections']

    def validate(self, attrs):
        if 'title' not in attrs:
            raise serializers.ValidationError('Title Field Missing!')
        if not attrs['title']:
            raise serializers.ValidationError('Title Field is Empty!')
        if len(attrs) > 1:
            raise serializers.ValidationError('Too Many Fields')
        return attrs
