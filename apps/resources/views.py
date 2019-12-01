import uuid

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from .models import Document, Section
from .serializers import DocumentSerializer, SectionSerializer, SectionSerializerForAPIVIewOfASpecificDocument


class DocumentListAPIView(GenericAPIView):
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
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    def get(self, request, doc_name):
        try:
            sections = self.get_queryset().filter(document__title=doc_name)
        except Section.DoesNotExist as e:
            return Response(data={'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        data = SectionSerializerForAPIVIewOfASpecificDocument(sections, many=True).data
        return Response(data={'sections': data}, status=status.HTTP_200_OK)

    def post(self, request, doc_name):
        try:
            document = Document.objects.get(title=doc_name)
        except Document.DoesNotExist as e:
            return Response(data={'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

        section = self.get_serializer(data=request.data)
        section.is_valid()
        instance = section.save()
        instance.document = document
        instance.save()
        return Response(data=section.data, status=status.HTTP_201_CREATED)


class SectionAPIView(GenericAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    def get(self, request, section_uuid):
        try:
            section = self.get_queryset().get(uuid=section_uuid)
        except (Section.DoesNotExist, Section.MultipleObjectsReturned) as e:
            return Response(data={'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        data = self.get_serializer(section).data
        return Response(data={'section': data}, status=status.HTTP_200_OK)

    def put(self, request, section_uuid):
        try:
            section = self.get_queryset().get(uuid=section_uuid)
        except Section.DoesNotExist as e:
            return Response(data={'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        section = self.get_serializer(instance=section, data=request.data)
        section.is_valid()
        section.save()
        return Response(data=section.data, status=status.HTTP_202_ACCEPTED)
