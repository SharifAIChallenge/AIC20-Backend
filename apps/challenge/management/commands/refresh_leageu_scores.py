from django.core.management.base import BaseCommand

from ...models import Challenge, Group
from apps.scoreboard.models import Row


class Command(BaseCommand):
    """ This command initializes the scoreboard
        for given challenge for valid teams.
    """
    help = 'Initialize Scoreboard'

    def add_arguments(self, parser):

        parser.add_argument(
            '--refresh',
            action='store_true',
            help='refresh whole scoreboard'
        )

        parser.add_argument(
            'id',
            nargs=1,
            type=int,
            help='group id',
        )

    def handle(self, *args, **options):
        if options.get('init'):
            self._handle_init_all(options)

    def _handle_init_all(self, options):
        if not options.get('id') or len(options.get('id')) != 1:
            print("Please Enter Command Like This: --refresh {group_id}")
        else:
            group_id = options.get('id')[0]
            try:
                group = Group.objects.get(id=group_id)
            except (Challenge.MultipleObjectsReturned, Challenge.DoesNotExist) as e:
                print(e)
                return
            group_scoreboard = group.scoreboard
            rows = Row.objects.filter(scoreboard_id=group_scoreboard.id)
            rows.update(score=2000.0, wins=0, loss=0, draws=0)
            for match in group.matches.all():
                print(match)
                match.update_match_team_score()
