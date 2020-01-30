from rest_framework.serializers import ModelSerializer

from . import models as faq_models


class AnswerSerializer(ModelSerializer):
    class Meta:
        model = faq_models.Answer
        fields = ['id', 'title', 'body', 'question']


class QuestionSerializer(ModelSerializer):
    answer = AnswerSerializer(read_only=True)

    class Meta:
        model = faq_models.Question
        fields = ['id', 'title', 'body', 'answer']
