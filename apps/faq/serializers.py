from rest_framework.serializers import ModelSerializer

from . import models as faq_models


class QuestionWithAnswerSerializer(ModelSerializer):
    class Meta:
        model = faq_models.QuestionWithAnswer
        exclude = ['id']
