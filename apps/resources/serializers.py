from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from django.conf import settings

from .models import Document, Section, Subsection


class SubtitleSerializer(ModelSerializer):
    class Meta:
        model = Subsection
        fields = ['subtitle_en', 'subtitle_fa']

    def validate(self, attrs):
        if 'subtitle_en' not in attrs:
            raise serializers.ValidationError('Subtitle Field Missing!')
        if not attrs['subtitle_en']:
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
        fields = ['uuid', 'title_en', 'title_fa', 'markdown', 'subtitles', 'link_to_colab']

    def validate(self, attrs):
        if 'title_en' not in attrs:
            raise serializers.ValidationError('Title Field Missing!')
        if 'markdown' not in attrs:
            raise serializers.ValidationError('Markdown Field Missing!')
        if not attrs['title_en']:
            raise serializers.ValidationError('Title Field is Empty')
        if not attrs['markdown']:
            raise serializers.ValidationError('Markdown Field is Empty')

        if len(attrs) > 2:
            raise serializers.ValidationError('Too Many Fields')
        return attrs


class DocumentSerializer(ModelSerializer):

    thumbnail = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ['id', 'title_en', 'title_fa', 'description_en', 'description_fa', 'thumbnail', 'file', 'time_to_read']

    def get_thumbnail(self, obj):
        return settings.MEDIA_URL + str(obj.thumbnail.name)

    def get_file(self, obj):
        return settings.MEDIA_URL + str(obj.file.name)

    def validate(self, attrs):
        if 'title_en' not in attrs:
            raise serializers.ValidationError('Title Field Missing!')
        if not attrs['title']:
            raise serializers.ValidationError('Title Field is Empty!')
        if len(attrs) > 1:
            raise serializers.ValidationError('Too Many Fields')
        return attrs
