from rest_framework import status, parsers
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ChallengeScoreBoard, GroupScoreBoard
from ..challenge.models import Challenge, ChallengeTypes, Group
from .serializers import ScoreBoardSerializer


class ChallengeScoreBoardAPIView(GenericAPIView):
    serializer_class = ScoreBoardSerializer

    def get(self, request):
        challenge = get_object_or_404(Challenge, type=ChallengeTypes.PRIMARY)
        data = self.get_serializer(ChallengeScoreBoard.get_scoreboard(challenge=challenge), many=True).data
        return Response(data={'scoreboard': data}, status=status.HTTP_200_OK)


class GroupScoreBoardAPIView(GenericAPIView):
    serializer_class = ScoreBoardSerializer

    def get(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        data = self.get_serializer(GroupScoreBoard.get_scoreboard(group=group), many=True).data
        return Response(data={'scoreboard': data}, status=status.HTTP_200_OK)
