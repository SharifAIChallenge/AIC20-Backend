from django.core.management.base import BaseCommand
from django.db.models import Sum

from ...models import Challenge, ChallengeTypes, GameTeam
from ....scoreboard.models import FriendlyScoreBoard, Row


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

    def handle(self, *args, **options):
        if options.get('init'):
            self._handle_init_all(options)

    def _handle_init_all(self, options):
        try:
            friendly_scoreboard = FriendlyScoreBoard.objects.get(id=1)
        except FriendlyScoreBoard.DoesNotExist:
            friendly_scoreboard = FriendlyScoreBoard.objects.create()
        challenge = Challenge.objects.get(type=ChallengeTypes.PRIMARY)
        for team in challenge.teams.all():
            if not friendly_scoreboard.rows.filter(team=team).exists():
                total_score = GameTeam.objects.filter(team=team).filter(game_side__game__match=None).aggregate(
                    total_score=Sum('score'))['total_score']
                wins, draws, loss = Stats
                Row.objects.create(team=team, scoreboard=friendly_scoreboard)
