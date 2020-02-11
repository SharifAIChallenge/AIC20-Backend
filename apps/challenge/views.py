from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import parsers
from django.utils.translation import ugettext_lazy as _
from apps.challenge.models import SubmissionStatusTypes
from . import models as challenge_models
from . import serializers as challenge_serializers


# Create your views here.

class ChallengesListAPIView(GenericAPIView):
    queryset = challenge_models.Challenge.objects.all()
    serializer_class = challenge_serializers.ChallengeSerializer

    def get(self, request):
        data = self.get_serializer(self.get_queryset(), many=True).data
        return Response(data={'challenges': data}, status=status.HTTP_200_OK)


class ChallengeDetailAPIView(GenericAPIView):
    queryset = challenge_models.Challenge.objects.all()
    serializer_class = challenge_serializers.ChallengeSerializer

    def get(self, request, challenge_id):
        challenge = get_object_or_404(self.get_queryset(), id=challenge_id)
        data = self.get_serializer(challenge).data
        return Response(data={'challenge': data}, status=status.HTTP_200_OK)


class TournamentsListAPIView(GenericAPIView):
    queryset = challenge_models.Tournament.objects.all()
    serializer_class = challenge_serializers.TournamentSerializer

    def get(self, request, challenge_id):
        challenge = get_object_or_404(challenge_models.Challenge, id=challenge_id)
        data = self.get_serializer(self.get_queryset().filter(challenge=challenge), many=True).data
        return Response(data={'challenge_id': challenge_id, 'tournaments': data}, status=status.HTTP_200_OK)


class TournamentDetailAPIView(GenericAPIView):
    queryset = challenge_models.Tournament.objects.all()
    serializer_class = challenge_serializers.TournamentSerializer

    def get(self, request, challenge_id, tournament_id):
        tournament = get_object_or_404(self.get_queryset(), id=tournament_id)
        data = self.get_serializer(tournament).data
        return Response(data={'tournament': data}, status=status.HTTP_200_OK)


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

    # TODO: only allow infra to change game result
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"ok": "true"})


class SubmissionSubmitAPIView(GenericAPIView):
    serializer_class = challenge_serializers.SubmissionPostSerializer
    parser_classes = (parsers.MultiPartParser,)

    def post(self, request):
        submission = self.get_serializer(data=request.data, context={'request': request})
        if submission.is_valid(raise_exception=True):
            submission = submission.save()
            return Response(
                data={'details': _('Submission information successfully submitted'), 'submission_id': submission.id})
        return Response(data={'errors': [_('Something Went Wrong')]}, status=status.HTTP_406_NOT_ACCEPTABLE)


class SubmissionsListAPIView(GenericAPIView):
    queryset = challenge_models.Submission.objects.all()
    serializer_class = challenge_serializers.SubmissionSerializer

    def get(self, request, team_id):
        data = self.get_serializer(self.get_queryset().filter(team_id=team_id), many=True).data
        return Response(data={'submissions': data}, status=status.HTTP_200_OK)


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
