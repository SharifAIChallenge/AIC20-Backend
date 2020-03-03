from django.core.management.base import BaseCommand

from ...models import Challenge, ChallengeTypes
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
            print("Please Enter Command Like This: --update {scoreboard_id}")
        else:
            scoreboard_id = options.get('id')[0]
            try:
                scoreboard = ScoreBoard.objects.get(id=scoreboard_id)
            except (ScoreBoard.MultipleObjectsReturned, ScoreBoard.DoesNotExist) as e:
                print(e)
                return
            main_scoreboard = scoreboard.group.stage.tournament.challenge.scoreboard
            if main_scoreboard and not scoreboard.calculated:
                for main_row in main_scoreboard.rows.all():
                    row = scoreboard.rows.filter(team=main_row.team).last()
                    if row:
                        main_row.score += (row.score - 2000)
                        main_row.wins += row.wins
                        main_row.loss += row.loss
                        main_row.draws += row.draws
                        main_row.save()
                scoreboard.calculated = True
                scoreboard.save()
