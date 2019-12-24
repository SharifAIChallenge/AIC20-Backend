from .views import HomepageView
from django.urls import include, path

urlpatterns = [
    path('', HomepageView.as_view())
]
