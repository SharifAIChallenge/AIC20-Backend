from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from apps.resources.authentications.authentication import TokenAuthentication
from .models import Document, Section
from .serializers import DocumentSerializer, SectionSerializer, SectionSerializerForAPIVIewOfASpecificDocument


class DocumentListAPIView(GenericAPIView):
    authentication_classes = [TokenAuthentication, ]

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get(self, request):
        data = self.get_serializer(self.get_queryset(), many=True).data
        return Response(data={'documents': data}, status=status.HTTP_200_OK)

    def post(self, request):
        document = DocumentSerializer(data=request.data)
        document.is_valid()
        document.save()
        return Response(data=document.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        document = DocumentSerializer(data=request.data)
        document.is_valid()
        document.save()
        return Response(data=document.data, status=status.HTTP_202_ACCEPTED)


class DocumentInstanceAPIView(GenericAPIView):
    authentication_classes = [TokenAuthentication, ]

    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    def get(self, request, doc_name):
        sections = self.get_queryset().filter(document__title=doc_name)
        data = SectionSerializerForAPIVIewOfASpecificDocument(sections, many=True).data
        return Response(data={'document_title': doc_name, 'sections': data}, status=status.HTTP_200_OK)

    def post(self, request, doc_name):
        document = get_object_or_404(self.get_queryset(), title=doc_name)
        section = self.get_serializer(data=request.data)
        section.is_valid()
        instance = section.save()
        instance.document = document
        instance.save()
        return Response(data=section.data, status=status.HTTP_201_CREATED)


class SectionAPIView(GenericAPIView):
    authentication_classes = [TokenAuthentication, ]

    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    def get(self, request, section_uuid):
        section = get_object_or_404(self.get_queryset(), uuid=section_uuid)
        data = self.get_serializer(section).data
        return Response(data={'document_title': section.document.title, 'section': data}, status=status.HTTP_200_OK)

    def put(self, request, section_uuid):
        section = get_object_or_404(self.get_queryset(), uuid=section_uuid)
        section = self.get_serializer(instance=section, data=request.data)
        section.is_valid()
        section.save()
        return Response(data=section.data, status=status.HTTP_202_ACCEPTED)
