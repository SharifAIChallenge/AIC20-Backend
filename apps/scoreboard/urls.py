from django.urls import path

from . import views

app_name = 'scoreboard'
urlpatterns = [
    path('challenge', views.ChallengeScoreBoardAPIView.as_view(), name='challenge_scoreboard'),
    # path('friendly', views.FriendlyScoreBoardAPIView.as_view(), name='friendly_scoreboard')
]
