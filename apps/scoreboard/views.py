from django.shortcuts import render
from rest_framework.generics import GenericAPIView


# Create your views here.

class ChallengesListAPIView(GenericAPIView):
    def get(self, request):
        pass


class ChallengeDetailAPIView(GenericAPIView):
    def get(self, request):
        pass


class TournamentsListAPIView(GenericAPIView):
    def get(self, request):
        pass


class TournamentDetailAPIView(GenericAPIView):
    def get(self, request):
        pass


class MatchesListAPIView(GenericAPIView):
    def get(self, request):
        pass


class MatchDetailAPIView(GenericAPIView):
    def get(self, request):
        pass


class GamesListAPIView(GenericAPIView):
    def get(self, request):
        pass


class GameDetailAPIView(GenericAPIView):
    def get(self, request):
        pass


class SubmitAPIView(GenericAPIView):
    def post(self, request):
        pass


class SubmissionsListAPIView(GenericAPIView):
    def get(self, request):
        pass
