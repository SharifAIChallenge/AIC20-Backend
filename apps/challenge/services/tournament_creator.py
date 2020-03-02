from random import random, shuffle

from django.utils import timezone

from apps.participation.models import Team
from apps.scoreboard.models import ChallengeScoreBoard, GroupScoreBoard
from ..models import Challenge, Tournament, TournamentTypes, Stage, Group, GroupTeam, Match, MatchTeam, MatchTypes, \
    Game, GameSide, GameTeam, Submission


class TournamentCreator:

    def __init__(self, tournament):
        self.score_board_rows = ChallengeScoreBoard.get_scoreboard_sorted_rows(tournament.challenge)
        self.tournament = tournament
        self.stage = ''
        self.group = ''
        self.games_ids = []
        pass

    def __call__(self):
        self._filter_teams()
        self._create_stages()
        self._create_groups()
        self.run_six_hour_tournament(match_map=self.tournament.tournament_map)
        return self.games_ids

    def _filter_teams(self):
        filtered_rows = []
        for row in self.score_board_rows:
            if Submission.objects.filter(team=row.team).filter(is_final=True).exists():
                filtered_rows.append(row.team)
        self.score_board_rows = filtered_rows

    def _create_stages(self):
        self.stage = Stage.objects.create(tournament=self.tournament)

    def _create_groups(self):
        self.group = Group.objects.create(stage=self.stage)
        GroupScoreBoard.objects.create(group=self.group)

    def run_six_hour_tournament(self, match_map):
        segmentation = self._get_segmentation()
        for rows_of_a_match in segmentation:
            match = Match(type=MatchTypes.DIFFERENT, group=self.group, map=match_map)
            self._create_match_teams(match, rows_of_a_match)
            self._create_games(match, rows_of_a_match)

    def permutations_for_single_match(self, rows, match_type=MatchTypes.DIFFERENT):
        if match_type == MatchTypes.SIMILAR:
            return [[rows[0], rows[0]], [rows[1], rows[1]]]
        return [[[rows[0], rows[1]], [rows[2], rows[3]]], [[rows[0], rows[2]], [rows[1], rows[3]]],
                [[rows[0], rows[3]], [rows[1], rows[2]]]]

    def _get_segmentation(self):
        segmentation = []
        while len(self.score_board_rows) > 4:
            first_eight_rows = self.score_board_rows[:8]
            shuffle(first_eight_rows)
            selection = first_eight_rows[:4]
            self.score_board_rows = [row for row in self.score_board_rows if row not in selection]
            segmentation.append(selection)
        selection = self.score_board_rows
        for i in range(4 - len(selection)):
            selection.append(None)
        return segmentation

    def _create_match_teams(self, match, rows_of_a_match):
        match_teams = []
        for row in rows_of_a_match:
            match_teams.append(MatchTeam(team=row.team, match=match))
        MatchTeam.objects.bulk_create(match_teams)
        match.save()

    def _create_games(self, match, rows):
        permutations_of_match = self.permutations_for_single_match(rows)
        for permutation in permutations_of_match:
            game = Game(match=match)
            self._create_game_side(game, permutation)
            game.save()
            self.games_ids.append(game.id)

    def _create_game_side(self, game, permutation):
        game_sides = []
        for side in permutation:
            game_side = GameSide(game=game)
            for row_of_side in side:
                GameTeam.objects.create(team=row_of_side.team, game_side=game_side)
            game_sides.append(game_side)
        GameSide.objects.bulk_create(game_sides)
