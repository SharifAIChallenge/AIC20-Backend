from django.urls import path

from . import views

app_name = 'challenge'

urlpatterns = [
    path('challenges/', views.ChallengesListAPIView.as_view(), name='challenges_list'),
    path('challenges/<int:challenge_id>', views.ChallengeDetailAPIView.as_view(), name='challenge_detail'),
    path('challenges/<int:challenge_id>/tournaments', views.TournamentsListAPIView.as_view(), name='tournaments_list'),
    path('challenges/<int:challenge_id>/tournaments/<int:tournament_id>', views.TournamentDetailAPIView.as_view(),
         name='tournament_detail'),
    path('submission/submit', views.SubmissionSubmitAPIView.as_view(),
         name='submit_submission'),
    path('submission/submissions', views.SubmissionsListAPIView.as_view(), name='team_submissions_list'),
    path('submission/change_final/<int:submission_id>', views.ChangeFinalSubmissionAPIView.as_view(),
         name='change_final_submission'),
    path('games', views.GamesListAPIView.as_view(), name='games_list'),
    path('game/report', views.report, name='infrastructure_report'),
    path('game/friendly', views.FriendlyGameAPIView.as_view(), name='friendly_match_request'),
    path('game/lobby', views.FriendlyMatchLobbyAPIView.as_view(), name='lobby'),
    path('game/stats', views.StatsAPIView.as_view(), name='games_stats')
]
