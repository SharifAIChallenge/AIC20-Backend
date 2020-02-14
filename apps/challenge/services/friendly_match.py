from apps.challenge.models import FriendlyGameTeam, FriendlyGame


class FriendlyGameCreator:

    def __init__(self, lobby):
        self.lobby = lobby
        self.friendly_game = ''
        self.friendly_game_teams = []

    def __call__(self, *args, **kwargs):
        self._create_friendly_game()
        self._create_friendly_game_teams()
        return self.friendly_game

    def _create_friendly_game(self):
        self.friendly_game = FriendlyGame.objects.create()

    def _create_friendly_game_teams(self):
        for team in self.lobby.teams.all():
            self.friendly_game_teams.append(
                FriendlyGameTeam.objects.create(team=team, friendly_game=self.friendly_game))
