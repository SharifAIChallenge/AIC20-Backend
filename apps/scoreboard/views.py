from rest_framework import status, parsers
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ChallengeScoreBoard, GroupScoreBoard, ScoreBoardTypes
from ..challenge.models import Challenge, ChallengeTypes, Group
from .serializers import RowSerializer


class ChallengeScoreBoardAPIView(GenericAPIView):
    serializer_class = RowSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        challenge = get_object_or_404(Challenge, type=ChallengeTypes.PRIMARY)
        data = self.get_serializer(ChallengeScoreBoard.get_scoreboard_sorted_rows(challenge=challenge), many=True).data
        return Response(data={'scoreboard': data}, status=status.HTTP_200_OK)

#
# class FriendlyScoreBoardAPIView(GenericAPIView):
#     serializer_class = RowSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         scoreboard = get_object_or_404(FriendlyScoreBoard, type=ScoreBoardTypes.FRIENDLY)
#         rows = scoreboard.rows.all().order_by('-score')
#         data = self.get_serializer(rows, many=True).data
#         return Response(data={'scoreboard': data}, status=status.HTTP_200_OK)
