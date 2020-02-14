import json

from django.http import JsonResponse
from rest_framework import status, parsers
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _

from apps.participation.models import Team, Participant
from apps.participation.services.answer_invitation import AnswerInvitation
from apps.participation.services.leave_team import LeaveTeam
from apps.participation.services.send_invitation import SendInvitation
from apps.scoreboard.models import Row
from . import models as participation_models
from . import serializers as participation_serializers
from django.shortcuts import get_object_or_404


class BadgeListAPIView(GenericAPIView):
    queryset = participation_models.Badge.objects.all()
    serializer_class = participation_serializers.BadgeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = self.get_serializer(self.get_queryset(), many=True).data
        return Response(data={'badges': data}, status=status.HTTP_200_OK)


class ParticipantListAPIView(GenericAPIView):
    queryset = participation_models.Participant.objects.all()
    serializer_class = participation_serializers.ParticipantSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = self.get_serializer(self.get_queryset(), many=True).data
        return Response(data={'participants': data}, status=status.HTTP_200_OK)


class SendInvitationAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        invitation_serializer, errors = SendInvitation(request=request)()
        if errors:
            return Response(data={'errors': errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(data={'invitation': invitation_serializer.data}, status=status.HTTP_200_OK)


class LeaveTeamAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        errors = LeaveTeam(request=request)()
        if errors:
            return Response(data={'errors': errors}, status=status.HTTP_200_OK)
        return Response(data={'details': _('You left your team successfully')}, status=status.HTTP_200_OK)


class AnswerInvitationAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, invitation_id):
        errors = AnswerInvitation(request=request, invitation_id=invitation_id)()
        if errors:
            return Response(data={'errors': errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(data={'details': _('You answered invitation successfully')}, status=status.HTTP_200_OK)


class InvitationsToMeAPIView(GenericAPIView):
    queryset = participation_models.Invitation.objects.all()
    serializer_class = participation_serializers.InvitationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = self.get_serializer(self.get_queryset().filter(target=self.request.user), many=True).data
        return Response(data={"invitations": data}, status=status.HTTP_200_OK)


class InvitationsToOthersAPIView(GenericAPIView):
    queryset = participation_serializers.Invitation.objects.all()
    serializer_class = participation_serializers.InvitationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = self.get_serializer(self.get_queryset().filter(source=self.request.user), many=True).data
        return Response(data={'invitations': data}, status=status.HTTP_200_OK)


class CreateTeamAPIView(GenericAPIView):
    serializer_class = participation_serializers.TeamPostSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (parsers.MultiPartParser,)

    def post(self, request):
        team = self.get_serializer(data=request.data)
        if team.is_valid(raise_exception=True):
            team = team.save()
        Participant.objects.create(user=request.user, team=team)
        Row.objects.create(team=team, scoreboard=team.challenge.scoreboard)
        return Response(data={'details': _('Team Created Successfully')}, status=status.HTTP_200_OK)


class TeamDetailAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = participation_serializers.TeamSerializer

    def get(self, request):
        team_name = request.GET.get('name', '')
        if team_name:
            team = get_object_or_404(Team, name=team_name)
        elif hasattr(request.user, 'participant'):
            team = request.user.participant.team
        else:
            return Response(data={'errors': ['Sorry! you dont have a team']})

        data = self.get_serializer(team).data
        return Response(data={'team': data}, status=status.HTTP_200_OK)
