from django.shortcuts import render
from apps.go.models import *
from rest_framework.exceptions import NotFound
from django.shortcuts import redirect

# Create your views here.
from rest_framework.generics import GenericAPIView


class RedirectView(GenericAPIView):

    def get(self, request, source):
        if Redirect.objects.filter(source=source).count() == 0:
            raise NotFound(detail="Error 404, page not found", code=404)

        destination = Redirect.objects.filter(source=source).get()

        return redirect(destination.destination)
