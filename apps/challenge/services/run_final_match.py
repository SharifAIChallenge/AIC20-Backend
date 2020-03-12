from apps.challenge.models import Game, GameSide, GameTeam
from apps.challenge.tasks import run_single_game


class RunFinalMatch:

    def __init__(self, first_team, second_team, maps):
        self.first_team = first_team
        self.second_team = second_team
        self.maps = maps
        self.games = []

    def __call__(self):
        self._create_games()
        self._create_game_sides()
        for game, game_map in zip(self.games, self.maps):
            run_single_game.delay(game.id, game_map.id)
        return self.games

    def _create_games(self):
        for i in range(len(self.maps)):
            self.games.append(Game.objects.create())

    def _create_game_sides(self):
        for game in self.games:
            game_side = GameSide.objects.create(game=game)
            GameTeam.objects.create(team=self.first_team, game_side=game_side)
            GameTeam.objects.create(team=self.first_team, game_side=game_side)
            game_side = GameSide.objects.create(game=game)
            GameTeam.objects.create(team=self.second_team, game_side=game_side)
            GameTeam.objects.create(team=self.second_team, game_side=game_side)
