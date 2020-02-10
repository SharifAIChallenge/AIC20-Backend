from django.urls import path, include
from rest_framework.authtoken import views
from apps.accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path('login', views.obtain_auth_token),
    path('signup', SignUpView.as_view()),
    path('resend-activation-link', ResendActivationEmailAPIView.as_view()),
    path('activate/<slug:eid>/<slug:token>', ActivateView.as_view()),
    path('logout', LogoutView.as_view()),
    path('profile', ProfileView.as_view()),
    path('password/change', ChangePasswordAPIView.as_view()),
    path('password/reset', ResetPasswordView.as_view()),
    path('password/reset/confirm', ResetPasswordConfirmView.as_view()),
    path('usercontext', UserContext.as_view())
]
