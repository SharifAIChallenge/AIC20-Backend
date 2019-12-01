from rest_framework.serializers import ModelSerializer, Serializer

from .models import Document, Section, Subtitle


class SubtitleSerializer(ModelSerializer):
    class Meta:
        model = Subtitle
        fields = ['subtitle']


class SectionSerializer(ModelSerializer):
    """
        Main Serializer fo Section Model
    """
    subtitles = SubtitleSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ['title', 'markdown', 'subtitles']


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
    sections_with_subtitles = SectionSerializerForDocument(many=True, read_only=True)

    class Meta:
        model = Document
        fields = ['title', 'sections_with_subtitles']
