from django.urls import path

from .views import DocumentListAPIView, DocumentInstanceAPIView, SectionAPIView

app_name = 'resource'

urlpatterns = [
    path('', DocumentListAPIView.as_view(), name='documents_list'),
    path('<int:doc_id>',
         DocumentInstanceAPIView.as_view(), name='document_sections'),
    path('sections/<section_uuid>', SectionAPIView.as_view(), name='section'),
]
