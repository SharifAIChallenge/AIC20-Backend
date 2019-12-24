from django.conf.urls import url
from django.urls import path
from apps.go.views import RedirectView


urlpatterns = [
    path('<slug:source>', RedirectView.as_view()),
]
