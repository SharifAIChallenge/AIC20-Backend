from django.urls import path

from . import views

app_name = 'participation'

urlpatterns = [
    path('badges/', views.BadgeListAPIView.as_view(), name='badge_list'),
    path('participants/', views.ParticipantListAPIView.as_view(), name='participant_list'),
    path('invitation/invite', views.SendInvitationAPIView.as_view(), name='send_invitation'),
    path('<str: team_name>/leave', views.LeaveTeamAPIView.as_view(), name='leave_team'),
    path('invitation/<int: invitation_id>', views.AnswerInvitationAPIView.as_view(), name='answer_invitation'),
]
