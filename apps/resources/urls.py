from django.urls import path

from .views import DocumentListAPIView, DocumentInstanceAPIView, SectionAPIView

app_name = 'resource'

urlpatterns = [
    path('documents/', DocumentListAPIView.as_view(), name='documents_list'),
    path('documents/<doc_name>/sections/',
         DocumentInstanceAPIView.as_view(), name='document_sections'),
    path('sections/<section_uuid>/', SectionAPIView.as_view(), name='section'),
]
