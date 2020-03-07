from rest_framework import status, parsers
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ChallengeScoreBoard, GroupScoreBoard, FriendlyScoreBoard, ScoreBoardTypes, ScoreBoard
from ..challenge.models import Challenge, ChallengeTypes, Group, GameTeam, TournamentTypes
from .serializers import RowSerializer, GroupScoreBoardSerializer


class ChallengeScoreBoardAPIView(GenericAPIView):
    serializer_class = RowSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        challenge = get_object_or_404(Challenge, type=ChallengeTypes.PRIMARY)
        teams_with_game_ids = GameTeam.objects.distinct('team_id').values_list('team_id')
        data = self.get_serializer(
            ChallengeScoreBoard.get_scoreboard_sorted_rows(challenge=challenge).filter(team_id__in=teams_with_game_ids),
            many=True).data
        return Response(data={'scoreboard': data}, status=status.HTTP_200_OK)


class FriendlyScoreBoardAPIView(GenericAPIView):
    serializer_class = RowSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        scoreboard = get_object_or_404(ScoreBoard, type=ScoreBoardTypes.FRIENDLY)
        teams_with_game_ids = GameTeam.objects.filter(game_side__game__match=None).distinct('team_id').values_list(
            'team_id')
        rows = scoreboard.rows.all().order_by('-score').filter(team_id__in=teams_with_game_ids)
        data = self.get_serializer(rows, many=True).data
        return Response(data={'scoreboard': data}, status=status.HTTP_200_OK)


class GroupScoreBoardAPIView(GenericAPIView):
    serializer_class = GroupScoreBoardSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        group_scoreboards = GroupScoreBoard.objects.filter(group__stage__tournament__type=TournamentTypes.LEAGUE)
        data = self.get_serializer(group_scoreboards, many=True).data
        return Response(data={'scoreboards': data}, status=status.HTTP_200_OK)
