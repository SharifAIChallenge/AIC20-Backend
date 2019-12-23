from django.urls import path, include

from apps.accounts.views import *
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('api/token', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('signup', SignUpView.as_view()),
    path('logout', LogoutView.as_view()),
    path('rest-auth/',  include('rest_auth.urls')),
    path('', include('django.contrib.auth.urls')),
]
