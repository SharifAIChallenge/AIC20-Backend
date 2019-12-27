from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from apps.accounts.serializer import *

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect


class SignUpView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if User.objects.filter(email=serializer.email).count() > 0:
            return Response({'error': 'A user with this email currently exists'}, status=400)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'detail': 'User created successfully'}, status=200)
        else:
            return Response({'error': 'Error occurred during User creation'}, status=500)


class LogoutView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class ResetPasswordView(GenericAPIView):

    def get(self, request, uid, token):
        return redirect(f'http://datadays.sharif.edu/forgot/reset?uid={uid}&token={token}')


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

