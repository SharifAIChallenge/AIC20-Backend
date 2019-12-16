from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.accounts.serializer import *
from apps.translation.util import translateQuerySet


class SignUpView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

    def get(self, request, username):
        filtered_queryset = translateQuerySet(self.get_queryset(), request).get(username=username)
        data = self.get_serializer(filtered_queryset)
        return Response(data=data, status=status.HTTP_200_OK)


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
