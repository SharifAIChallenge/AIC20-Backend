import codecs
import json
import logging

from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
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
from apps.challenge.models import Submission, Lobby, Game, SingleGameStatusTypes

from apps.challenge.services.lobby_handler import LobbyHandler
from apps.challenge.services.stats import Stats
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


class GamesListAPIView(GenericAPIView):
    queryset = challenge_models.Game.objects.all()
    serializer_class = challenge_serializers.GameSerializer

    def get(self, request):
        if not hasattr(request.user, 'participant'):
            return Response(data={'errors': ['Sorry! you dont have a team']}, status=status.HTTP_406_NOT_ACCEPTABLE)
        try:
            offset = int(request.GET.get('offset', 0))
            count = int(request.GET.get('count', 50))
        except ValueError:
            offset = 0
            count = 50
        team = request.user.participant.team
        time_limit = team.challenge.end_time
        game_ids = challenge_models.GameTeam.objects.filter(team=team).values_list(
            'game_side__game_id', flat=True)
        query = self.get_queryset().filter(id__in=game_ids).filter(time__gte=time_limit).order_by('-time')
        data = self.get_serializer(query[offset * count: offset * count + count], many=True).data
        return Response(data={'count': query.count(), 'games': data}, status=status.HTTP_200_OK)


class StatsAPIView(GenericAPIView):
    queryset = challenge_models.GameTeam.objects.all()

    def get(self, request):
        if not hasattr(request.user, 'participant'):
            return Response(data={'errors': ['Sorry! you dont have a team']}, status=status.HTTP_406_NOT_ACCEPTABLE)
        wins, draws, loss = Stats(team=request.user.participant.team)()
        return Response(data={'wins': wins, 'draws': draws, 'loss': loss}, status=status.HTTP_200_OK)


class SubmissionSubmitAPIView(GenericAPIView):
    serializer_class = challenge_serializers.SubmissionPostSerializer
    parser_classes = (parsers.MultiPartParser,)

    def post(self, request):
        if not hasattr(request.user, 'participant'):
            return Response(data={'errors': ['Sorry! you dont have a team']}, status=status.HTTP_406_NOT_ACCEPTABLE)
        submission = self.get_serializer(data=request.data, context={'request': request})
        if submission.is_valid(raise_exception=True):
            submission = submission.save()
            return Response(
                data={'details': _('Submission information successfully submitted'), 'submission_id': submission.id},
                status=status.HTTP_200_OK)
        return Response(data={'errors': [_('Something Went Wrong')]}, status=status.HTTP_406_NOT_ACCEPTABLE)


class SubmissionSubmitSecondMethodAPIView(GenericAPIView):
    serializer_class = challenge_serializers.SubmissionSecondMethodPostSerializer

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
        if not hasattr(request.user, 'participant'):
            return Response(data={'errors': ['Sorry! you dont have a team']}, status=status.HTTP_406_NOT_ACCEPTABLE)
        challenge = challenge_models.Challenge.objects.filter(type=challenge_models.ChallengeTypes.FINAL).last()
        if not challenge.can_change_submission:
            return Response(data={'errors': ['Submission change is closed!']})
        submission = get_object_or_404(Submission, id=submission_id)
        try:
            submission.set_final()
            return Response(data={'details': 'Final submission changed successfully'}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(data={'errors': [str(e)]}, status=status.HTTP_406_NOT_ACCEPTABLE)


class FriendlyGameAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = challenge_serializers.GameSerializer
    queryset = challenge_models.Game.objects.all()

    def get(self, request):
        if not hasattr(request.user, 'participant'):
            return Response(data={'errors': ['Sorry! you dont have a team']}, status=status.HTTP_406_NOT_ACCEPTABLE)
        game_ids = challenge_models.GameTeam.objects.filter(team=self.request.user.participant.team).filter(
            game_side__game__match=None).values_list('game_side__game', flat=True)
        data = self.get_serializer(self.get_queryset().filter(id__in=game_ids).order_by('-time')[:50], many=True).data
        return Response(data={'games': data}, status=status.HTTP_200_OK)

    def post(self, request):

        if not hasattr(request.user, 'participant'):
            return Response(data={'errors': ['Sorry! you dont have a team']}, status=status.HTTP_406_NOT_ACCEPTABLE)

        errors, friendly_game = LobbyHandler(request=request)()
        if errors:
            return Response(data={'errors': errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if friendly_game:
            from apps.challenge.tasks import run_single_game
            try:
                run_single_game.delay(friendly_game.id)
            except Exception as e:
                friendly_game.status = SingleGameStatusTypes.FAILED
                friendly_game.save()
                return Response(data={'errors': [str(e)]}, status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response(data={'details': 'gameRunned'})
        return Response(data={'details': 'your request submitted'})


class FriendlyMatchLobbyAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = challenge_serializers.LobbySerializer

    def get(self, request):
        if not hasattr(request.user, 'participant'):
            return Response(data={'errors': ['Sorry! you dont have a team']}, status=status.HTTP_406_NOT_ACCEPTABLE)
        queryset = list(request.user.participant.team.lobbies1.filter(
            completed=False)) + list(request.user.participant.team.lobbies2.filter(completed=False))

        data = self.get_serializer(queryset, many=True).data
        return Response(data={'lobbies': data}, status=status.HTTP_200_OK)


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
                        graphic_log = functions.download_file(single_report['parameters']['code_log'])
                        print("infrastructure code log file downloaded")
                    except Exception as e:
                        logger.error('Error while download log of compile: %s' % e)
                        return HttpResponseServerError()
                    log = json.loads(graphic_log.text, strict=False)
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
            submit.infra_compile_message = 'Unknown error occurred maybe compilation timed out'
            logger.exception(error)
            submit.save()
            return JsonResponse({'success': False})
        submit.save()
        return JsonResponse({'success': True})
    elif single_report['operation'] == 'run':
        try:
            game = Game.objects.get(infra_token=single_report['id'])
            if game.status == SingleGameStatusTypes.DONE:
                return JsonResponse({'success': True})
            logger.debug("Obtained relevant single match")
        except Exception as exception:
            logger.exception(exception)
            return JsonResponse({'success': False})
        if single_report['status'] == 2:
            logger.debug("Report status is OK")
            graphic_log = functions.download_file(single_report['parameters']['graphic_log'])
            client0_log = functions.download_file(single_report['parameters']['client1_log'])
            client1_log = functions.download_file(single_report['parameters']['client2_log'])
            client2_log = functions.download_file(single_report['parameters']['client3_log'])
            client3_log = functions.download_file(single_report['parameters']['client4_log'])

            game.log = ContentFile(name=single_report['parameters']['graphic_log'] + ".json", content=graphic_log.text)

            try:
                game.update_scores_and_client_logs(client0_log, single_report['parameters']['client1_log'],
                                                   client1_log, single_report['parameters']['client2_log'],
                                                   client2_log, single_report['parameters']['client3_log'],
                                                   client3_log, single_report['parameters']['client4_log'])
            except Exception as e:
                game.infra_game_message = str(e)
                game.status = 'failed'
                game.save()
                return JsonResponse({'success': False, 'error': 'Maybe log file Error.'})
        elif single_report['status'] == 3:
            game.status = 'failed'
            game.infra_game_message = single_report['log']
        else:
            return JsonResponse({'success': False, 'error': 'Invalid Status.'})

        game.save()
        return JsonResponse({'success': True})
    return HttpResponseServerError()
