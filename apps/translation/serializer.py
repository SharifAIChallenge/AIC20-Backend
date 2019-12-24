from .models import TranslatedText, DocumentTest, TText
from rest_framework import serializers


class TranslatedTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslatedText
        fields = ('content_en', 'content_fa')


class TTextSerializer(serializers.ModelSerializer):

    class Meta:
        model = TText
        fields = ['en', 'fa']


class DocumentTestSerializer(serializers.ModelSerializer):
    title_value = serializers.CharField()
    description_value = serializers.CharField()

    class Meta:
        model = DocumentTest
        fields = ('description_value', 'title_value')
