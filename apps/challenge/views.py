import codecs
import json
import logging

from django.conf import settings
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseServerError
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import parsers
from django.utils.translation import ugettext_lazy as _
from django.db import transaction

from apps.challenge import functions
from apps.challenge.models import Submission, Lobby
from apps.challenge.services.friendly_match import FriendlyGameCreator
from . import models as challenge_models
from . import tasks
from . import serializers as challenge_serializers

logger = logging.getLogger(__name__)


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
                data={'details': _('Submission information successfully submitted'), 'submission_id': submission.id},
                status=status.HTTP_200_OK)
        return Response(data={'errors': [_('Something Went Wrong')]}, status=status.HTTP_406_NOT_ACCEPTABLE)


class SubmissionsListAPIView(GenericAPIView):
    queryset = challenge_models.Submission.objects.all()
    serializer_class = challenge_serializers.SubmissionSerializer

    def get(self, request):
        if not hasattr(request.user, 'participant'):
            return Response(data={'errors': ['Sorry! you dont have a team']}, status=status.HTTP_406_NOT_ACCEPTABLE)
        data = self.get_serializer(self.get_queryset().filter(team=request.user.participant.team),
                                   many=True).data
        return Response(data={'submissions': data}, status=status.HTTP_200_OK)


class ChangeFinalSubmissionAPIView(GenericAPIView):

    def put(self, request, submission_id):
        submission = get_object_or_404(Submission, id=submission_id)
        try:
            submission.set_final()
            return Response(data={'details': 'Final submission changed successfully'}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(data={'errors': [str(e)]}, status=status.HTTP_406_NOT_ACCEPTABLE)


class FriendlyMatchRequestAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not hasattr(request.user, 'participant'):
            return Response(data={'errors': ['Sorry! you dont have a team']})
        with transaction.atomic():
            # try:
            #     lobby = Lobby.objects.get(completed=False)
            # except (Lobby.DoesNotExist, Lobby.MultipleObjectsReturned) as e:
            #     lobby = Lobby.objects.create()
            lobby = Lobby.objects.filter(completed=False).last()
            lobby = lobby if lobby else Lobby.objects.create()
            lobby.teams.add(request.user.participant.team)
            if lobby.teams.count() >= 4:
                lobby.completed = True
                lobby.save()
                friendly_game = FriendlyGameCreator(lobby=lobby)()
                tasks.run_friendly_game.delay(friendly_game.id)
                return Response(data={'details': 'Friendly match runned!'})
            return Response(data={'details': 'your request submitted'})


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


@csrf_exempt
def report(request):
    print("infrastructure called me :)))))")
    if request.META.get('HTTP_AUTHORIZATION') != settings.INFRA_AUTH_TOKEN:
        return HttpResponseBadRequest()
    print("infrastructure Authorized")
    single_report = json.loads(request.body.decode("utf-8"), strict=False)
    print("infrastructure json body parsed")
    if single_report['operation'] == 'compile':
        print("infrastructure compile operation")
        if Submission.objects.filter(infra_compile_token=single_report['id']).count() != 1:
            logger.error('Error while finding team submission in report view')
            return JsonResponse({'success': False})

        submit = Submission.objects.get(infra_compile_token=single_report['id'])
        print("infrastructure got submission object")
        try:
            if single_report['status'] == 2:
                submit.infra_compile_token = single_report['parameters'].get('code_compiled_zip', None)
                if submit.status == 'compiling':
                    try:
                        logfile = functions.download_file(single_report['parameters']['code_log'])
                        print("infrastructure code log file downloaded")
                    except Exception as e:
                        logger.error('Error while download log of compile: %s' % e)
                        return HttpResponseServerError()

                    reader = codecs.getreader('utf-8')

                    log = json.load(logfile.text, strict=False)
                    if len(log["errors"]) == 0:
                        print("infrastructure compiled successfully")
                        submit.status = 'compiled'
                        submit.set_final()
                    else:
                        print("compile errors: ")
                        print(log["errors"])
                        submit.status = 'failed'
                        submit.infra_compile_message = '...' + '<br>'.join(error for error in log["errors"])[-1000:]
            elif single_report['status'] == 3:
                print("infrastructure unkown error occurred while compiling")
                submit.status = 'failed'
                submit.infra_compile_message = 'Unknown error occurred maybe compilation timed out'
        except BaseException as error:
            submit.status = 'failed'
            submit.infra_compile_message = str(logfile) + "  " + logfile.text + "  " + str(logfile.raw)
            logger.exception(error)
            submit.save()
            return JsonResponse({'success': False})
        submit.save()
        return JsonResponse({'success': True})
    # elif single_report['operation'] == 'run':
    #     try:
    #         single_match = SingleMatch.objects.get(infra_token=single_report['id'])
    #         logger.debug("Obtained relevant single match")
    #     except Exception as exception:
    #         logger.exception(exception)
    #         return JsonResponse({'success': False})
    #
    #     try:
    #         if single_report['status'] == 2:
    #             logger.debug("Report status is OK")
    #             logfile = functions.download_file(single_report['parameters']['graphic_log'])
    #             client1_log_token = single_report['parameters']['client1_log']
    #             client2_log_token = single_report['parameters']['client2_log']
    #             client1_log_file = functions.download_file(client1_log_token)
    #             client2_log_file = functions.download_file(client2_log_token)
    #
    #             single_match.status = 'done'
    #             single_match.log.save(name='log', content=File(logfile.file))
    #             single_match.part1_log.save(name='client.zip', content=File(client1_log_file.file))
    #             single_match.part2_log.save(name='client.zip', content=File(client2_log_file.file))
    #             single_match.update_scores_from_log()
    #         elif single_report['status'] == 3:
    #             single_match.status = 'failed'
    #             single_match.infra_match_message = single_report['log']
    #         else:
    #             return JsonResponse({'success': False, 'error': 'Invalid Status.'})
    #     except BaseException as error:
    #         logger.exception(error)
    #         single_match.status = 'failed'
    #         single_match.save()
    #         return JsonResponse({'success': False})
    #
    #     single_match.save()
    #     return JsonResponse({'success': True})
    return HttpResponseServerError()
