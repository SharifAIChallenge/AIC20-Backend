from rest_framework.serializers import ModelSerializer

from .models import Document, Section, Subtitle


class DocumentSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = ['title']


class SectionSerializer(ModelSerializer):
    pass


class SubtitleSerializer(ModelSerializer):
    class Meta:
        model = Subtitle
        fields = ['subtitle']
