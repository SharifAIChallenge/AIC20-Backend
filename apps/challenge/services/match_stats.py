from apps.challenge.models import GameTeam, Game, SingleGameStatusTypes


class MatchStats:

    def __init__(self, match, team, just_group_scoreboard=False):
        self.match = match
        self.team = team
        self.wins = 0
        self.draws = 0
        self.loss = 0
        self.just_group_scoreboard = just_group_scoreboard

    def __call__(self, *args, **kwargs):
        self._wins()
        self._loss_and_draws()
        return self.wins, self.draws, self.loss

    def _wins(self):
        self.wins = GameTeam.objects.filter(team=self.team)
        if self.just_group_scoreboard:
            self.wins = self.wins.filter(game_side__game__match__group=self.match.group)
        else:
            self.wins = self.wins.filter(game_side__game__match=self.match)
        self.wins = self.wins.filter(game_side__game__status=SingleGameStatusTypes.DONE).filter(
            game_side__has_won=True).count()

    def _loss_and_draws(self):
        other_games = GameTeam.objects.filter(team=self.team)
        if self.just_group_scoreboard:
            other_games = other_games.filter(game_side__game__match__group=self.match.group)
        else:
            other_games = other_games.filter(game_side__game__match=self.match)
        other_games = other_games.filter(game_side__game__status=SingleGameStatusTypes.DONE).filter(
            game_side__has_won=False).values_list('game_side__game_id', flat=True)

        other_games = Game.objects.filter(id__in=other_games)
        for game in other_games:
            if game.game_sides.filter(has_won=False).count() >= 2:
                self.draws += 1
            else:
                self.loss += 1
