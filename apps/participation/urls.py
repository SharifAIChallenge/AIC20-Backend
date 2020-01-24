from django.urls import path

from . import views

app_name = 'participation'

urlpatterns = [
    path('badges/', views.BadgeListAPIView.as_view(), name='badge_list'),
    path('participants/', views.ParticipantListAPIView.as_view(), name='participant_list'),
]
