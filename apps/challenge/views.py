from django.shortcuts import render
from rest_framework.generics import GenericAPIView

from . import models as challenge_models
from . import serializers as challenge_serializers


# Create your views here.

class ChallengesListAPIView(GenericAPIView):
    queryset = challenge_models.Challenge.objects.all()
    serializer_class = challenge_serializers.ChallengeSerializer

    def get(self, request):
        pass


class ChallengeDetailAPIView(GenericAPIView):
    queryset = challenge_models.Challenge.objects.all()
    serializer_class = challenge_serializers.ChallengeSerializer

    def get(self, request):
        pass


class TournamentsListAPIView(GenericAPIView):
    queryset = challenge_models.Tournament.objects.all()
    serializer_class = challenge_serializers.TournamentSerializer

    def get(self, request):
        pass


class TournamentDetailAPIView(GenericAPIView):
    queryset = challenge_models.Tournament.objects.all()
    serializer_class = challenge_serializers.TournamentSerializer

    def get(self, request):
        pass


class MatchesListAPIView(GenericAPIView):
    queryset = challenge_models.Match
    serializer_class = challenge_serializers.MatchSerializer

    def get(self, request):
        pass


class MatchDetailAPIView(GenericAPIView):
    queryset = challenge_models.Match
    serializer_class = challenge_serializers.MatchSerializer

    def get(self, request):
        pass


class GamesListAPIView(GenericAPIView):
    queryset = challenge_models.Game
    serializer_class = challenge_serializers.GameSerializer

    def get(self, request):
        pass


class GameDetailAPIView(GenericAPIView):
    queryset = challenge_models.Game
    serializer_class = challenge_serializers.GameSerializer

    def get(self, request):
        pass


class SubmitAPIView(GenericAPIView):
    serializer_class = challenge_serializers.SubmissionSerializer
    
    def post(self, request):
        pass


class SubmissionsListAPIView(GenericAPIView):
    queryset = challenge_models.Submission
    serializer_class = challenge_serializers.SubmissionSerializer

    def get(self, request):
        pass


class MapsListAPIView(GenericAPIView):
    queryset = challenge_models.Map
    serializer_class = challenge_serializers.MapSerializer

    def get(self, request):
        pass


class MapDetailAPIView(GenericAPIView):
    queryset = challenge_models.Map
    serializer_class = challenge_serializers.MapSerializer

    def get(self, request):
        pass
