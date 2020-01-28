from apps.challenge.models import GameTeam, Submission
from apps.participation.models import Team


class TeamDashBoard:
    def __init__(self, team: Team):
        self.team = team

    def count_of_submit(self) -> int:
        return Submission.objects.count(team=self.team)

    def count_of_win(self) -> int:
        result = 0
        game_teams = GameTeam.objects.filter(team=self.team)
        for game_team in game_teams:
            if game_team.game_side.has_won:
                result += 1

        return result

    def participated_tournaments(self) -> list:
        tournaments_name = []
        for tournament in self.team.tournament.all():
            tournaments_name.append(tournament.name)

        return tournaments_name
