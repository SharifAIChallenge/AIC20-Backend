from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Document, Section
from .serializers import DocumentSerializer, SectionSerializer


class DocumentListAPIView(GenericAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = self.get_serializer(self.get_queryset().order_by('order'), many=True).data
        return Response(data={'documents': data}, status=status.HTTP_200_OK)


class DocumentInstanceAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, doc_id):
        doc = get_object_or_404(Document.objects.all(), pk=doc_id)
        data = DocumentSerializer(doc).data
        data['sections'] = SectionSerializer(Section.objects.filter(document=doc).order_by('order'), many=True).data
        return Response(data, status=status.HTTP_200_OK)


class SectionAPIView(GenericAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, section_uuid):
        section = get_object_or_404(self.get_queryset(), uuid=section_uuid)
        data = self.get_serializer(section).data
        return Response(data={
            'document_title': section.document.title_en,
            'section': data
        }, status=status.HTTP_200_OK)
