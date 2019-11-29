from django.urls import path

from .views import DocumentAPIView, SectionAPIView

urlpatterns = [
    path('documents/', ),
    path('documents/<doc_name>/sections'),
    path('documents/<doc_name>/<section_uuid>'),
]