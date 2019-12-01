from django.urls import path

from apps.user_profile.views import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view())
]