from django.urls import path

from apps.notification.views import NotificationView

urlpatterns = [
    path('notifications/', NotificationView.as_view(), name='notifications_list'),

]
