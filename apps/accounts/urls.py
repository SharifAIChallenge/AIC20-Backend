from django.urls import path, include

from rest_framework_simplejwt import views as jwt_views

from apps.accounts.views import *


urlpatterns = [
    path('login', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('refresh', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('signup', SignUpView.as_view()),
    path('activate/<slug:eid>/<slug:token>', ActivateView.as_view()),
    path('logout', LogoutView.as_view()),
    path('profile', ProfileView.as_view()),
    path('password/change/', ChangePasswordAPIView.as_view()),
    path('password/reset/', ResetPasswordView.as_view()),
    path('password/reset/confirm/', ResetPasswordConfirmView.as_view()),

]

