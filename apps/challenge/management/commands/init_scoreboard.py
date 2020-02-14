from django.core.management.base import BaseCommand

from ...models import Challenge
from ....scoreboard.models import ScoreBoard, Row


class Command(BaseCommand):
    """ This command initializes the scoreboard
        by created milestones.
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
            nargs='{1}',
            type=int,
            help='Task or milestone ids',
        )

    def handle(self, *args, **options):
        if options.get('init'):
            self._handle_init_all(options)

    def _handle_init_all(self, options):
        if not options.get('id') or len(options.get('id')) != 2:
            print("Please Enter Command Like This: --init {Challenge_id}")
        else:
            challenge_id = options.get('id')
            try:
                challenge = Challenge.objects.get(id=challenge_id)
            except (Challenge.MultipleObjectsReturned, Challenge.DoesNotExist) as e:
                print(e)
                return

            for team in challenge.teams.all():
                Row.objects.create(team=team, scoreboard=challenge.scoreboard)
