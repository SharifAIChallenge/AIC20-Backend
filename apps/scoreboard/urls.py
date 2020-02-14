from django.urls import path

from . import views

app_name = 'scoreboard'
urlpatterns = [
    path('challenge', views.ChallengeScoreBoardAPIView.as_view(), name='challenge_scoreboard'),
    path('group/<group_id>', views.GroupScoreBoardAPIView.as_view(), name='group_scoreboard')
]
