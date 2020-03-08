from django.core.management.base import BaseCommand

from ...models import Challenge
from ....scoreboard.models import ScoreBoard, Row, GroupScoreBoard


class Command(BaseCommand):
    """ This command initializes the scoreboard
        for given challenge for valid teams.
    """
    help = 'Initialize Scoreboard'

    def add_arguments(self, parser):

        parser.add_argument(
            '--refresh',
            action='store_true',
            help='initialize whole scoreboard'
        )

        parser.add_argument(
            'id',
            nargs=1,
            type=int,
            help='group scoreboard id',
        )

    def handle(self, *args, **options):
        if options.get('init'):
            self._handle_init_all(options)

    def _handle_init_all(self, options):
        if not options.get('id') or len(options.get('id')) != 1:
            print("Please Enter Command Like This: --refresh {group_scoreboard_id}")
        else:
            group_scoreboard_id = options.get('id')[0]
            try:
                group_scoreboard = GroupScoreBoard.objects.get(id=group_scoreboard_id)
            except (Challenge.MultipleObjectsReturned, Challenge.DoesNotExist) as e:
                print(e)
                return
            group_scoreboard.rows.all().update(score=2000.0, wins=0, loss=0, draws=0)
            for match in group_scoreboard.group.matches.all():
                match.update_match_team_score()
