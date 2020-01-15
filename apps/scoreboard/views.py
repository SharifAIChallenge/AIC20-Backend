from django.shortcuts import render
from rest_framework.generics import GenericAPIView


# Create your views here.

class Submit(GenericAPIView):
    def post(self, request):
        pass


class MatchList(GenericAPIView):
    def get(self, request):
        pass
