from django.core.management.base import BaseCommand
from django.db.models import Sum

from apps.challenge.services.stats import Stats
from apps.challenge.services.utils import update_game_team_scoreboard_score
from ...models import Challenge, ChallengeTypes, GameTeam, Game
from ....scoreboard.models import FriendlyScoreBoard, Row, ScoreBoardTypes, ScoreBoard


class Command(BaseCommand):
    """ This command initializes the scoreboard
        for given challenge for valid teams.
    """
    help = 'Initialize Scoreboard'

    def add_arguments(self, parser):

        parser.add_argument(
            '--init',
            action='store_true',
            help='initialize whole scoreboard'
        )

        parser.add_argument(
            '--refresh_score',
            action='store_true',
            help='initialize whole scoreboard'
        )

    def handle(self, *args, **options):
        if options.get('init'):
            self._handle_init_all(options)
        elif options.get('refresh_score'):
            self._handle_refresh(options)

    def _handle_init_all(self, options):
        try:
            friendly_scoreboard = ScoreBoard.objects.get(type=ScoreBoardTypes.FRIENDLY)
        except FriendlyScoreBoard.DoesNotExist:
            friendly_scoreboard = FriendlyScoreBoard.objects.create()
        challenge = Challenge.objects.get(type=ChallengeTypes.PRIMARY)
        for team in challenge.teams.all():
            if not friendly_scoreboard.rows.filter(team=team).exists():
                total_score = GameTeam.objects.filter(team=team).filter(game_side__game__match=None).aggregate(
                    total_score=Sum('score'))['total_score']
                wins, draws, loss = Stats(team=team, friendly_only=True)()
                Row.objects.create(team=team, scoreboard=friendly_scoreboard, score=total_score if total_score else 0,
                                   wins=wins, loss=loss,
                                   draws=draws)

    def _handle_refresh(self, refresh):
        try:
            friendly_scoreboard = ScoreBoard.objects.get(type=ScoreBoardTypes.FRIENDLY)
        except FriendlyScoreBoard.DoesNotExist:
            friendly_scoreboard = FriendlyScoreBoard.objects.create()
        games = Game.objects.filter(status='done').filter(match=None).order_by(
            'time')
        friendly_scoreboard.rows.all().update(score=1000.0)
        for game in games:
            update_game_team_scoreboard_score(game, friendly_scoreboard)
        for row in friendly_scoreboard.rows:
            row.wins, row.draws, row.loss = Stats(team=row.team, friendly_only=True)
            row.save()
