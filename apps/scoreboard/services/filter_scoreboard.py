from apps.challenge.models import GameTeam
from apps.scoreboard.models import ChallengeScoreBoard


class FilterScoreboard:

    def __init__(self, challenge):
        self.challenge = challenge
        self.initial_rows = ChallengeScoreBoard.get_scoreboard_sorted_rows(challenge=challenge)

    def _filter_rows(self):
        game_teams = GameTeam.objects.distinct('team_id').values_list('team_id')

