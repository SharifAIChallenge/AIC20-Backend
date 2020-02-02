import json

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _

from apps.participation.models import Team, Participant
from apps.participation.services.answer_invitation import AnswerInvitation
from apps.participation.services.dashboard import TeamDashBoard
from apps.participation.services.leave_team import LeaveTeam
from apps.participation.services.send_invitation import SendInvitation
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
            return Response(data={'errors': json.dumps(errors)}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(data={'invitation': invitation_serializer.data}, status=status.HTTP_200_OK)


class LeaveTeamAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, team_name):
        errors = LeaveTeam(request=request, team_name=team_name)()
        if errors:
            return Response(data={'errors': json.dumps(errors)}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(data={'details': _('You left your team successfully')}, status=status.HTTP_200_OK)


class AnswerInvitationAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, invitation_id):
        errors = AnswerInvitation(request=request, invitation_id=invitation_id)()
        if errors:
            return Response(data={'errors': json.dumps(errors)}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(data={'details': _('You answered invitation successfully')}, status=status.HTTP_200_OK)


class InvitationsToMeAPIView(GenericAPIView):
    queryset = participation_models.Invitation.objects.all()
    serializer_class = participation_serializers.InvitationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = self.get_serializer(self.get_queryset().filter(target=self.request.usesr)).data
        return Response(data={"invitations": data}, status=status.HTTP_200_OK)


class InvitationsToOthersAPIView(GenericAPIView):
    queryset = participation_serializers.Invitation.objects.all()
    serializer_class = participation_serializers.InvitationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = self.get_serializer(self.get_queryset().filter(source=self.request.user)).data
        return Response(data={'invitations': data}, status=status.HTTP_200_OK)


class CreateTeamAPIView(GenericAPIView):
    serializer_class = participation_serializers.TeamSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        team = self.get_serializer(data=request.body)
        if team.is_valid(raise_exception=True):
            team = team.save()
        Participant.objects.create(user=request.user, team=team)
        return Response(data={'details': _('Team Created Successfully')}, status=status.HTTP_200_OK)


class TeamDetailAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        participant = get_object_or_404(Participant, user=request.user)
        team = participant.team
        if team is None:
            return Response(data={'errors': json.dumps([_('Sorry! You are not participated in any team')])},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        data = TeamDashBoard(team)()
        return Response(data={'team_info': json.dumps(data)}, status=status.HTTP_200_OK)
