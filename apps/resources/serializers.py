from rest_framework.serializers import ModelSerializer

from .models import Document, Section, Subtitle


class SubtitleSerializer(ModelSerializer):
    class Meta:
        model = Subtitle
        fields = ['subtitle']


class SectionSerializer(ModelSerializer):
    pass


class DocumentSerializer(ModelSerializer):
    """
    set init for section
    """
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = ['title', 'sections']
