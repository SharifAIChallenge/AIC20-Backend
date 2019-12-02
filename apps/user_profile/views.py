
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login

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
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        return Response(request.data)


class LogoutView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        pass

    def post(self, request):
        pass


class ForgotPasswordView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        pass

    def post(self, request):
        pass


class LoginWithGoogleView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        pass

    def post(self, request):
        pass
