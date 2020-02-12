from django.urls import path

from . import views

app_name = 'challenge'

urlpatterns = [
    path('stats', views.StatsAPIView.as_view(), name='challenge_stats'),
    path('challenges/', views.ChallengesListAPIView.as_view(), name='challenges_list'),
    path('challenges/<int:challenge_id>', views.ChallengeDetailAPIView.as_view(), name='challenge_detail'),
    path('challenges/<int:challenge_id>/tournaments', views.TournamentsListAPIView.as_view(), name='tournaments_list'),
    path('challenges/<int:challenge_id>/tournaments/<int:tournament_id>', views.TournamentDetailAPIView.as_view(),
         name='tournament_detail'),
    path('submission/submit/information', views.SubmissionSubmitAPIView.as_view(),
         name='submit_submission_information'),
    path('submission/submissions/<int:team_id>', views.SubmissionsListAPIView.as_view(), name='team_submissions_list'),
    path('game/<int:game_id>', views.GameDetailAPIView.as_view()),
    # path('report', )
]
