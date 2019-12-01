from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from .models import Document, Section
from .serializers import DocumentSerializer, SectionSerializer, SectionSerializerForAPIVIewOfASpecificDocument, \
    SubtitleSerializer


class DocumentListAPIView(GenericAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get(self, request):
        data = self.get_serializer(self.get_queryset(), many=True).data
        return Response(data={'documents': data}, status=status.HTTP_200_OK)

    def post(self, request):
        document = DocumentSerializer(data=request.data)
        if document.is_valid(True):
            document.save()
            return Response(data=document.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        document = DocumentSerializer(data=request.data)
        if document.is_valid(True):
            document.save()
            return Response(data=document.data, status=status.HTTP_202_ACCEPTED)


class DocumentInstanceAPIView(GenericAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    def get(self, request, doc_name):
        sections = self.get_queryset().filter(document__title=doc_name)
        data = SectionSerializerForAPIVIewOfASpecificDocument(sections, many=True).data
        return Response(data={'document_title': doc_name, 'sections': data}, status=status.HTTP_200_OK)

    def post(self, request, doc_name):
        document = get_object_or_404(Document, title=doc_name)
        section = self.get_serializer(data=request.data)
        if section.is_valid(True):
            instance = section.save()
            instance.document = document
            instance.save()
            return Response(data=SectionSerializerForAPIVIewOfASpecificDocument(instance).data,
                            status=status.HTTP_201_CREATED)


class SectionAPIView(GenericAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    def get(self, request, section_uuid):
        section = get_object_or_404(self.get_queryset(), uuid=section_uuid)
        data = self.get_serializer(section).data
        return Response(data={'document_title': section.document.title, 'section': data}, status=status.HTTP_200_OK)

    def post(self, request, section_uuid):
        section = get_object_or_404(self.get_queryset(), uuid=section_uuid)
        subtitle = SubtitleSerializer(data=request.data)
        if subtitle.is_valid(True):
            instance = subtitle.save()
            instance.section = section
            instance.save()
            return Response(data=subtitle.data, status=status.HTTP_201_CREATED)

    def put(self, request, section_uuid):
        section = get_object_or_404(self.get_queryset(), uuid=section_uuid)
        section = self.get_serializer(instance=section, data=request.data)
        if section.is_valid(True):
            section.save()
            return Response(data=section.data, status=status.HTTP_202_ACCEPTED)
