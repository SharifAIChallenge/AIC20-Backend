from django.core.management.base import BaseCommand

from ...models import Challenge
from ....scoreboard.models import ScoreBoard, Row


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
            'id',
            nargs=1,
            type=int,
            help='challenge id',
        )

    def handle(self, *args, **options):
        if options.get('init'):
            self._handle_init_all(options)

    def _handle_init_all(self, options):
        if not options.get('id') or len(options.get('id')) != 1:
            print("Please Enter Command Like This: --init {Challenge_id}")
        else:
            challenge_id = options.get('id')[0]
            try:
                challenge = Challenge.objects.get(id=challenge_id)
            except (Challenge.MultipleObjectsReturned, Challenge.DoesNotExist) as e:
                print(e)
                return

            for team in challenge.teams.all():
                if team.is_valid:
                    Row.objects.create(team=team, scoreboard=challenge.scoreboard)
