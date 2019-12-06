from django.shortcuts import render
from .models import DocumentTest
from .serializer import DocumentTestSerializer
from django.db.models import F
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .util import translateQuerySet

class DocumentInstanceAPIView(GenericAPIView):
    queryset = DocumentTest.objects.all()
    serializer_class = DocumentTestSerializer

    def get(self, request, pk):
        document = translateQuerySet(self.get_queryset(), request.headers['Accept-language'], ['title', 'description']).filter(pk=pk)
        data = self.get_serializer(document, many = True).data
        return Response(data=data, status=status.HTTP_200_OK)
