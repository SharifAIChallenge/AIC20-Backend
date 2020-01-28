from django.urls import path

from . import views

app_name = 'challenge'

urlpatterns = [
    path('challenges/', views.ChallengesListAPIView.as_view(), name='challenges_list'),
    path('submission/submit/information', views.SubmissionSubmitAPIView.as_view(),
         name='submit_submission_information'),
    path('submission/submissions/<int:team_id>', views.SubmissionsListAPIView.as_view(), name='team_submissions_list'),
    path('game/<int:game_id>', views.GameDetailAPIView.as_view()),
]
