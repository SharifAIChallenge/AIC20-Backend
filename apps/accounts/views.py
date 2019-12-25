from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from apps.accounts.serializer import *

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


class SignUpView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'detail': 'User created successfully'})
        else:
            return Response({'detail': 'Error occurred during User creation'})


class LogoutView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class ForgotPasswordView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def post(self, request):
        pass


class LoginWithGoogleView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def post(self, request):
        pass


class ProfileView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserViewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'user is not authenticated'})
        data = self.get_serializer(user).data['profile']
        return Response(data=data, status=HTTP_200_OK)

    def put(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'user is not authenticated'})
        user_serializer = UserViewSerializer(user)
        user_serializer.update(user, request.data)
        return Response(user_serializer.data)
