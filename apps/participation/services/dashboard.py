from typing import Dict, Union

from apps.challenge.models import GameTeam, Submission
from apps.participation.models import Team


class TeamDashBoard:
    def __init__(self, team: Team):
        self.team = team
        self.count_of_submit = 0
        self.count_of_win = 0
        self.participated_tournaments = 0

    def __call__(self):
        self._count_of_submit()
        self._count_of_win()
        # self._participated_tournaments()
        return self._serialize_data()

    def _count_of_submit(self) -> None:
        self.count_of_submit = Submission.objects.filter(team=self.team).count()

    def _count_of_win(self) -> None:
        result = 0
        game_teams = GameTeam.objects.filter(team=self.team)
        for game_team in game_teams:
            if game_team.game_side.has_won:
                result += 1

        self.count_of_win = result

    # def _participated_tournaments(self) -> None:
    #     tournaments_name = []
    #     for tournament in self.team.tournament.all():
    #         tournaments_name.append(tournament.name)
    #
    #     self.participated_tournaments = tournaments_name

    def _serialize_data(self) -> Dict[str, Union[int, str]]:
        return {
            'submits_count': self.count_of_submit,
            'wins_count': self.count_of_win,
            # 'tournaments_participated': self.participated_tournaments,
        }
