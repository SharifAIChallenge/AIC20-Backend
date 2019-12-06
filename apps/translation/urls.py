from rest_framework import routers
from .views import DocumentInstanceAPIView
from django.urls import include, path

urlpatterns = [
  path('<int:pk>/', DocumentInstanceAPIView.as_view())
]