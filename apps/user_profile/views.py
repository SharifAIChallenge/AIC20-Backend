from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, logout
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_400_BAD_REQUEST

from apps.user_profile.models import Profile
from apps.user_profile.serializer import UserSerializer


class SignUpView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)


class LoginView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=HTTP_400_BAD_REQUEST)
        users = Profile.objects.filter(username=username, password=password)
        if len(users) == 0:
            return Response({'error': 'Invalid Credentials'},
                            status=HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=users[0])
        return Response({'token': token.key},
                        status=HTTP_200_OK)


class LogoutView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class ForgotPasswordView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        pass


class LoginWithGoogleView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        pass
