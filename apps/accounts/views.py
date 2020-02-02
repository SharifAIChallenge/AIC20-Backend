import secrets
import base64

from django.conf import settings
from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.timezone import now

from apps.accounts.serializer import *
from apps.accounts.models import ResetPasswordToken, ActivateUserToken
from apps.challenge.models import Challenge
from apps.challenge.serializers import ChallengeSerializer


class SignUpView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            print(settings.EMAIL_BACKEND)
            activate_user_token = ActivateUserToken(
                token=secrets.token_urlsafe(32),
                eid=urlsafe_base64_encode(force_bytes(serializer.validated_data['email'])),
            )
            activate_user_token.save()

            context = {
                'domain': 'aichallenge.sharif.edu',
                'eid': activate_user_token.eid,
                'token': activate_user_token.token,
            }
            email_html_message = render_to_string('accounts/email/user_activate_email.html', context)
            email_plaintext_message = render_to_string('accounts/email/user_activate_email.txt', context)
            msg = EmailMultiAlternatives(
                _("Activate Account for {title}".format(title="AI Challenge")),
                email_plaintext_message,
                "sharif.aichallenge@gmail.com",
                [serializer.validated_data['email']]
            )
            msg.attach_alternative(email_html_message, "text/html")
            try:
                msg.send()

                serializer.save()
                serializer.instance.is_active = False
                serializer.instance.save()
            except Exception as e:
                print(e)
                print(serializer.validated_data['email'])
                return Response({'detail': 'Invalid email or user has not been saved.'}, status=406)

            return Response({'detail': 'User created successfully. Check your email for confirmation link'}, status=200)
        else:
            return Response({'error': 'Error occurred during User creation'}, status=500)


class ActivateView(GenericAPIView):

    def get(self, request, eid, token):
        activate_user_token = get_object_or_404(ActivateUserToken,
                                                eid=eid, token=token)

        email = urlsafe_base64_decode(activate_user_token.eid).decode('utf-8')
        user = get_object_or_404(User, email=email)
        user.is_active = True
        user.save()

        return redirect('http://aichallenge.sharif.edu/login')


class LogoutView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        print(request.user, request.user.is_authenticated, request.user.is_active)
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class ResetPasswordView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        data = self.get_serializer(request.data).data

        user = get_object_or_404(User, email=data['email'])

        uid = urlsafe_base64_encode(force_bytes(user.id))
        ResetPasswordToken.objects.filter(uid=uid).delete()
        reset_password_token = ResetPasswordToken(
            uid=uid,
            token=secrets.token_urlsafe(32),
            expiration_date=timezone.now() + timezone.timedelta(hours=24),
        )
        reset_password_token.save()

        context = {
            'domain': 'aichallenge.sharif.edu',
            'username': user.username,
            'uid': reset_password_token.uid,
            'token': reset_password_token.token,
        }
        email_html_message = render_to_string('accounts/email/user_reset_password.html', context)
        email_plaintext_message = render_to_string('accounts/email/user_reset_password.txt', context)
        msg = EmailMultiAlternatives(
            _("Password Reset for {title}".format(title="AI Challenge")),
            email_plaintext_message,
            "aichallenge.sharif@gmail.com",
            [user.email]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()

        return Response({'detail': 'Successfully Sent Reset Password Email'}, status=200)


class ResetPasswordConfirmView(GenericAPIView):
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request):
        data = self.get_serializer(request.data).data

        rs_token = get_object_or_404(ResetPasswordToken, uid=data['uid'], token=data['token'])
        if (timezone.now() - rs_token.expiration_date).total_seconds() > 24 * 60 * 60:
            return Response({'error': 'Token Expired'}, status=400)

        user = get_object_or_404(User, id=urlsafe_base64_decode(data['uid']).decode('utf-8'))
        user.password = make_password(data['new_password1'])
        user.save()
        return Response({'detail': 'Successfully Changed Password'}, status=200)


class ProfileView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserViewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        data = self.get_serializer(user).data
        return Response(data=data, status=HTTP_200_OK)

    def put(self, request):
        user = request.user
        user_serializer = UserViewSerializer(user)
        user_serializer.update(user, request.data)
        return Response(user_serializer.data)


class ChangePasswordAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data

        if not request.user.check_password(data['old_password']):
            return Response({'detail': 'incorrect current password'}, status=406)

        request.user.password = make_password(data['new_password1'])
        request.user.save()
        return Response({'detail': 'password changed successfully'}, status=200)

class UserContext(GenericAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_challange = Challenge.objects.filter(
            start_time__lt= now(),
            end_time__gt= now(),
        )
        if current_challange.count() != 0:
            current_challange = ChallengeSerializer(current_challange.first()).data
        else:
            current_challange = {}
        return Response({
            'profile': UserSerializer(request.user).data,
            'can_submit': True, 
            #TODO: vaghti pool ezafe shod bazi vaghta false e
            'current_challange': current_challange,
        })