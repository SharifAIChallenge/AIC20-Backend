from django.shortcuts import render
from apps.go.models import *
from rest_framework.exceptions import NotFound
from django.shortcuts import redirect

from rest_framework.generics import GenericAPIView


class RedirectView(GenericAPIView):

    def get(self, request, source):

        r = Redirect.objects.filter(source=source)
        if r.count() != 1:
            raise NotFound(detail="Error 404, page not found", code=404)

        r = r.get()
        r.hits = r.hits + 1
        r.save()

        return redirect(r.destination)

