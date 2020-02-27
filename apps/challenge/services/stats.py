class Stats:

    def __init__(self, request):
        self.request = request
        self.wins = 0
        self.loss = 0
        self.draws = 0

    def __call__(self):
        self._wins()
        self._loss_and_draws()
        return self.wins, self.draws, self.loss

    def _wins(self):
        from apps.challenge.models import GameTeam

        self.wins = GameTeam.objects.filter(team=self.request.user.participant.team).filter(
            game_side__has_won=True).count()

    def _loss_and_draws(self):
        from apps.challenge.models import GameTeam, Game
        other_games = GameTeam.objects.filter(team=self.request.user.participant.team).filter(
            game_side__has_won=False).values_list('game_side__game_id', flat=True)
        other_games = Game.objects.filter(id__in=other_games)
        for game in other_games:
            if game.game_sides.filter(has_won=False).count() >= 2:
                self.draws += 1
            else:
                self.loss += 1
