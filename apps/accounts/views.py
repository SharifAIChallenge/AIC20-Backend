import secrets
import base64

from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from apps.accounts.serializer import *
from apps.accounts.models import ResetPasswordToken


class SignUpView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if User.objects.filter(email=serializer.initial_data['email']).count() > 0:
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

    def get(self, request, email):
        user = get_object_or_404(User, email=email)

        reset_password_token = ResetPasswordToken(
                uid=base64.b64encode(user.id).decode('ascii'),
                token=secrets.token_urlsafe(32),
                expiration_date=timezone.now() + timezone.timedelta(hours=24),
            )
        reset_password_token.save()

        context = {
            'domain': 'datadays.sharif.edu',
            'username': user.username,
            'uid': reset_password_token.uid,
            'token': reset_password_token.token,
        }

        email_html_message = render_to_string('accounts/email/user_reset_password.html', context)
        email_plaintext_message = render_to_string('accounts/email/user_reset_password.txt', context)

        msg = EmailMultiAlternatives(
                # title:
                _("Password Reset for {title}".format(title="DataDays")),
                # message:
                email_plaintext_message,
                # from:
                "datadays.sharif@gmail.com",
                # to:
                [user.email]
            )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()

    def post(self, request):
        try:
            new_password1 = request.data['new_password1']
            new_password2 = request.data['new_password2']
            uid = request.data['uid']
            token = request.data['token']
        except:
            return Response({'error': 'Bad Request'}, status=400)
        if new_password1 != new_password2:
            return Response({'error': 'Passwords missmatch'}, status=400)

        rs_token = get_object_or_404(ResetPasswordToken, uid=uid, token=token)
        if (timezone.now() - rs_token.expiration_date).total_seconds() > 24 * 60 * 60:
            return Response({'error': 'Token Expired'}, status=400)

        user = get_object_or_404(User, id=base64.b64decode(uid).decode('ascii'))
        user.password = make_password(new_password1)
        user.save()
        return Response({'detail': 'Successfully Changed Password'}, status=200)


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

