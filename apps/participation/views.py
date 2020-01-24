import json

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.participation.services.answer_invitation import AnswerInvitation
from apps.participation.services.leave_team import LeaveTeam
from apps.participation.services.send_invitation import SendInvitation
from . import models as participation_models
from . import serializers as participation_serializers


class BadgeListAPIView(GenericAPIView):
    queryset = participation_models.Badge.objects.all()
    serializer_class = participation_serializers.BadgeSerializer

    def get(self, request):
        data = self.get_serializer(self.get_queryset(), many=True).data
        return Response(data={'badges': data}, status=status.HTTP_200_OK)


class ParticipantListAPIView(GenericAPIView):
    queryset = participation_models.Participant.objects.all()
    serializer_class = participation_serializers.ParticipantSerializer

    def get(self, request):
        data = self.get_serializer(self.get_queryset(), many=True).data
        return Response(data={'participants': data}, status=status.HTTP_200_OK)


class SendInvitationAPIView(GenericAPIView):

    def post(self, request):
        invitation_serializer, errors = SendInvitation(request=request)()
        if errors:
            return Response(data={'errors': json.dumps(errors)}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(data={'invitation': invitation_serializer.data}, status=status.HTTP_200_OK)


class LeaveTeamAPIView(GenericAPIView):

    def post(self, request, team_name):
        errors = LeaveTeam(request=request, team_name=team_name)
        if errors:
            return Response(data={'errors': json.dumps(errors)}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(data={'details': 'You left your team successfully'}, status=status.HTTP_200_OK)


class AnswerInvitationAPIView(GenericAPIView):

    def post(self, request, invitation_id):
        errors = AnswerInvitation(request=request, invitation_id=invitation_id)
        if errors:
            return Response(data={'errors': json.dumps(errors)}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(data={'details': 'You answered invitation successfully'}, status=status.HTTP_200_OK)
