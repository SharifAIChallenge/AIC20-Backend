
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

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

    def get(self, request):
        pass

    def post(self, request):
        pass


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