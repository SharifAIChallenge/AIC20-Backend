from django.shortcuts import get_object_or_404
from rest_framework import status

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from . import serializers as faq_serializers
from . import models as faq_models


# Create your views here.

class QuestionsListAPIView(GenericAPIView):
    queryset = faq_models.Question.objects.all()
    serializer_class = faq_serializers.QuestionSerializer

    def get(self, request):
        data = self.get_serializer(self.get_queryset(), many=True).data
        return Response(data={'questions': data}, status=status.HTTP_200_OK)
