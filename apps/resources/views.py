from django.shortcuts import render
from rest_framework.response import Response

from rest_framework.views import APIView

from .models import Document
from .serializers import DocumentSerializer, SectionSerializer, SubtitleSerializer


class Document(APIView):

    def get(self, request):
        pass

    def post(self, request):
        pass

    def put(self, request):
        pass


class Section(APIView):

    def get(self, request):
        pass

    def post(self, request):
        pass

    def put(self, request):
        pass
