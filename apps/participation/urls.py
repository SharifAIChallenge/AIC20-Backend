from django.urls import path

from . import views

app_name = 'participation'

urlpatterns = [
    path('badges/', views.BadgeListAPIView.as_view(), name='badge_list'),
    path('participants/', views.ParticipantListAPIView.as_view(), name='participant_list'),
    path('invitation/invite', views.SendInvitationAPIView.as_view(), name='send_invitation'),
    path('invitation/<int:invitation_id>', views.AnswerInvitationAPIView.as_view(), name='answer_invitation'),
    path('invitation/invitations-to-me', views.InvitationsToMeAPIView.as_view(), name='invitations_to_me'),
    path('invitation/invitations-to-others', views.InvitationsToOthersAPIView.as_view(), name='invitations_to_others'),
    path('team/leave', views.TeamAPIView.as_view(), name='leave_team'),
    path('team/detail', views.TeamAPIView.as_view(), name='team_detail'),
    path('team/create', views.TeamAPIView.as_view(), name='create_team'),
    path('team/update', views.TeamAPIView.as_view(), name='update_team'),
]
