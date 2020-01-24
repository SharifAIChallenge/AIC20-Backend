from django.urls import path

from . import views

app_name = 'challenge'

urlpatterns = [
    path('challenges/', views.ChallengesListAPIView.as_view(), name='challenges_list'),
]
