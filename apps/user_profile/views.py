from django.shortcuts import render, redirect
from django.contrib.auth.admin import User
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.user_profile.serializer import UserSerializer


class SignUpView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        pass

    def post(self, request):
        pass


class LoginView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        pass

    def post(self, request):
        pass


class LogoutView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        pass

    def post(self, request):
        pass


class ForgotPasswordView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        pass

    def post(self, request):
        pass


class LoginWithGoogleView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        pass

    def post(self, request):
        pass