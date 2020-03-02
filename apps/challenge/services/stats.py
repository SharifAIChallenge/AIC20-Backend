class Stats:

    def __init__(self, team, friendly_only=False):
        self.team = team
        self.friendly_only = friendly_only
        self.wins = 0
        self.loss = 0
        self.draws = 0

    def __call__(self):
        self._wins()
        self._loss_and_draws()
        return self.wins, self.draws, self.loss

    def _wins(self):
        from apps.challenge.models import GameTeam

        game_teams = GameTeam.objects.filter(team=self.team).filter(
            game_side__has_won=True)
        if self.friendly_only:
            game_teams = game_teams.filter(game_side__game__match=None)
        self.wins = game_teams.count()

    def _loss_and_draws(self):
        from apps.challenge.models import GameTeam, Game
        other_games = GameTeam.objects.filter(team=self.team).filter(
            game_side__has_won=False)
        if self.friendly_only:
            other_games = other_games.filter(game_side__game__match=None)
        other_games = other_games.values_list('game_side__game_id', flat=True)

        other_games = Game.objects.filter(id__in=other_games)
        for game in other_games:
            if game.game_sides.filter(has_won=False).count() >= 2:
                self.draws += 1
            else:
                self.loss += 1
