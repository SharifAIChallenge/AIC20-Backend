import json

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


class TeamAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (parsers.MultiPartParser,)

    def get(self, request):
        team_name = request.GET.get('name', '')
        if team_name:
            team = get_object_or_404(Team, name=team_name)
            data = participation_serializers.LimitedTeamSerializer(team).data
        elif hasattr(request.user, 'participant'):
            team = request.user.participant.team
            data = participation_serializers.TeamSerializer(team).data
        else:
            return Response(data={'errors': ['Sorry! you dont have a team']})

        return Response(data={'team': data}, status=status.HTTP_200_OK)

    def post(self, request):
        team = participation_serializers.TeamPostSerializer(data=request.data)
        if team.is_valid(raise_exception=True):
            team = team.save()
        Participant.objects.create(user=request.user, team=team)
        Row.objects.create(team=team, scoreboard=team.challenge.scoreboard)
        return Response(data={'details': _('Team Created Successfully')}, status=status.HTTP_200_OK)

    def put(self, request):
        if not hasattr(request.user, 'participant'):
            return Response(data={'errors': ['Sorry you dont have any team']}, status=status.HTTP_406_NOT_ACCEPTABLE)
        team = request.user.participant.team
        updated_team = participation_serializers.TeamPutSerializer(instance=team, data=request.data)
        if updated_team.is_valid(raise_exception=True):
            updated_team.save()
        return Response(data={'details': 'Team updated successfully'})

    def delete(self, request):
        errors = LeaveTeam(request=request)()
        if errors:
            return Response(data={'errors': errors}, status=status.HTTP_200_OK)
        return Response(data={'details': _('You left your team successfully')}, status=status.HTTP_200_OK)
