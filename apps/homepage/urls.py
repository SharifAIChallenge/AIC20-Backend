from .views import HomepageView, TermsOfUseView
from django.urls import include, path

urlpatterns = [
    path('', HomepageView.as_view()),
    path('terms', TermsOfUseView.as_view())
]
