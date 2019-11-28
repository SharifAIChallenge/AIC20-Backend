from django.shortcuts import render
from rest_framework.response import Response

from rest_framework.generics import GenericAPIView

from .models import Document, Section, Subtitle
from .serializers import DocumentSerializer, SectionSerializer, SubtitleSerializer


class DocumentAPIView(GenericAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get(self, request):
        data = self.get_serializer(self.get_queryset, many=True).data
        return Response(data)

    def post(self, request):
        # document = DocumentSerializer(data=request.data)
        # document.is_valid()
        # document.save()
        # return Response(document.data)
        pass

    def put(self, request):
        pass


class SectionAPIView(GenericAPIView):

    def get(self, request):
        pass

    def post(self, request):
        pass

    def put(self, request):
        pass
