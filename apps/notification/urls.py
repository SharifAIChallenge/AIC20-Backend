from django.urls import path

from apps.notification.views import NotificationView, SubscriberView

urlpatterns = [
    path('', NotificationView.as_view(), name='notifications_list'),
    path('email', SubscriberView.as_view(), name='subscribe'),

]
