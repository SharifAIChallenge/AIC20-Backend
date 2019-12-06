from .models import TranslatedText, DocumentTest
from rest_framework import serializers


class TranslatedTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslatedText
        fields = ('content_en', 'content_fa')


class DocumentTestSerializer(serializers.ModelSerializer):
    title_value = serializers.CharField()
    description_value = serializers.CharField()

    class Meta:
        model = DocumentTest
        fields = ('description_value', 'title_value')
