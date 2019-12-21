from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from django.contrib.auth import authenticate, logout
from rest_framework.status import HTTP_200_OK

from apps.accounts.models import Profile
from apps.accounts.serializer import *

from django_rest_passwordreset.signals import reset_password_token_created
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



"""
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(reverse('password_reset:reset-password-request'),
                                                   reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
"""

