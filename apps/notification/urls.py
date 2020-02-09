from django.urls import path

from apps.notification.views import NotificationView, SubscriberView, PublicNotificationsAPIView

urlpatterns = [
    path('', NotificationView.as_view(), name='notifications_list'),
    path('public-notifications', PublicNotificationsAPIView.as_view(), name='public_notifications_list'),
    path('email', SubscriberView.as_view(), name='subscribe'),

]
