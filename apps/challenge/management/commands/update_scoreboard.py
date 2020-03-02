from django.core.management.base import BaseCommand

from ...models import Challenge
from ....scoreboard.models import ScoreBoard, Row, ChallengeScoreBoard, GroupScoreBoard


class Command(BaseCommand):
    """ This command initializes the scoreboard
        for given challenge for valid teams.
    """
    help = 'Initialize Scoreboard'

    def add_arguments(self, parser):

        parser.add_argument(
            '--update',
            action='store_true',
            help='update main scoreboard'
        )

        parser.add_argument(
            'id',
            nargs='1',
            type=int,
            help='scoreboards',
        )

    def handle(self, *args, **options):
        if options.get('update'):
            self._handle_init_all(options)

    def _handle_init_all(self, options):
        if not options.get('id') or len(options.get('id')) != 1:
            print("Please Enter Command Like This: --init {scoreboard}")
        else:
            scoreboard_id = options.get('id')[0]
            main_scoreboard = ChallengeScoreBoard.objects.filter(freeze=False).last()
            try:
                scoreboard = GroupScoreBoard.objects.get(id=scoreboard_id)
            except (ScoreBoard.MultipleObjectsReturned, ScoreBoard.DoesNotExist) as e:
                print(e)
                return
            if main_scoreboard:


            for team in challenge.teams.all():
                if team.is_valid:
                    Row.objects.create(team=team, scoreboard=challenge.scoreboard)
