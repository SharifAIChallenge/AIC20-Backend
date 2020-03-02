from random import random, shuffle

from django.utils import timezone

from apps.participation.models import Team
from apps.scoreboard.models import ChallengeScoreBoard, GroupScoreBoard
from ..models import Challenge, Tournament, TournamentTypes, Stage, Group, GroupTeam, Match, MatchTeam, MatchTypes, \
    Game, GameSide, GameTeam, Submission


class TournamentCreator:

    def __init__(self, tournament):
        self.score_board: ChallengeScoreBoard = ChallengeScoreBoard.objects.get(challenge=tournament.challenge)
        self.teams = self.score_board.rows.values_list('team', flat=True)
        self.teams = Team.objects.filter(id__in=self.teams)
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
        filtered_teams = []
        for team in self.teams:
            if Submission.objects.filter(team=team).filter(is_final=True).exists():
                filtered_teams.append(team)
        self.team = filtered_teams

    def _create_stages(self):
        self.stage = Stage.objects.create(tournament=self.tournament)

    def _create_groups(self):
        self.group = Group.objects.create(stage=self.stage)
        GroupScoreBoard.objects.create(group=self.group)

    def random_four_numbers(self, max_number):
        random_numbers = []
        while len(random_numbers) < 4:
            random_number = (random() * max_number)
            if random_number not in random_numbers:
                random_numbers.append(random_number)
        return random_numbers

    def permutations_for_single_match(self, teams, match_type=MatchTypes.DIFFERENT):
        if match_type == MatchTypes.SIMILAR:
            return [[teams[0], teams[0]], [teams[1], teams[1]]]
        return [[[teams[0], teams[1]], [teams[2], teams[3]]], [[teams[0], teams[2]], [teams[1], teams[3]]],
                [[teams[0], teams[3]], [teams[1], teams[2]]]]

    def run_six_hour_tournament(self, match_map):
        segmentation = self._get_segmentation()
        for teams_of_a_match in segmentation:
            match = Match(type=MatchTypes.DIFFERENT, group=self.group, map=match_map)
            self._create_match(match, teams_of_a_match)
            self._create_games(match, teams_of_a_match)

    def _get_segmentation(self):
        segmentation = []
        while len(self.teams) > 4:
            first_eight_team = self.teams[:8]
            shuffle(first_eight_team)
            selection = first_eight_team[:4]
            self.teams = [team for team in self.teams if team not in selection]
            segmentation.append(selection)
        selection = self.teams
        for i in range(4 - len(selection)):
            selection.append(None)
        return segmentation

    def _create_match(self, match, teams_of_a_match):
        match_teams = []
        for team in teams_of_a_match:
            match_teams.append(MatchTeam(team=team, match=match))
        MatchTeam.objects.bulk_create(match_teams)
        match.save()

    def _create_games(self, match, teams):
        permutations_of_match = self.permutations_for_single_match(teams)
        for permutation in permutations_of_match:
            game = Game(match=match)
            self._create_game_side(game, permutation)
            game.save()
            self.games_ids.append(game.id)

    def _create_game_side(self, game, permutation):
        game_sides = []
        for side in permutation:
            game_side = GameSide(game=game)
            for team_of_side in side:
                GameTeam.objects.create(team=team_of_side, game_side=game_side)
            game_sides.append(game_side)
        GameSide.objects.bulk_create(game_sides)
