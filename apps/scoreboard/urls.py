from django.urls import path

from . import views

app_name = 'scoreboard'
urlpatterns = [
    path('challenge/<int:challenge_id>', views.ChallengeScoreBoardAPIView.as_view(), name='challenge_scoreboard'),
    path('friendly', views.FriendlyScoreBoardAPIView.as_view(), name='friendly_scoreboard'),
    path('league', views.GroupScoreBoardAPIView.as_view(), name='league_scoreboard')
]
