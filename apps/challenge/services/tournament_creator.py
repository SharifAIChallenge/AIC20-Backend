from random import random, shuffle

from django.utils import timezone

from apps.participation.models import Team
from apps.scoreboard.models import ChallengeScoreBoard, GroupScoreBoard, Row
from ..models import Challenge, Tournament, TournamentTypes, Stage, Group, GroupTeam, Match, MatchTeam, MatchTypes, \
    Game, GameSide, GameTeam, Submission


class TournamentCreator:

    def __init__(self, tournament):
        self.rows = ChallengeScoreBoard.get_scoreboard_sorted_rows(tournament.challenge)
        self.teams = []
        self.bot_teams = []
        self.tournament = tournament
        self.stage = ''
        self.group = ''
        self.games_ids = []
        pass

    def __call__(self):
        self._get_bot_teams()
        self._filter_teams()
        self._create_stages()
        self._create_groups()
        self.run_six_hour_tournament(match_map=self.tournament.tournament_map)
        return self.games_ids

    def _get_bot_teams(self):
        self.bot_teams.append(Team.objects.get(name='ufo1'))
        self.bot_teams.append(Team.objects.get(name='ufo2'))
        self.bot_teams.append(Team.objects.get(name='ufo3'))

    def _filter_teams(self):
        filtered_teams = []
        for row in self.rows:
            if Submission.objects.filter(team=row.team).filter(
                    is_final=True).exists() and row.team.name not in ['ufo1', 'ufo2', 'ufo3']:
                filtered_teams.append(row.team)
        self.teams = filtered_teams

    def _create_stages(self):
        self.stage = Stage.objects.create(tournament=self.tournament)

    def _create_groups(self):
        self.group = Group.objects.create(stage=self.stage)
        group_scoreboard = GroupScoreBoard.objects.create(group=self.group)
        for team in self.teams:
            Row.objects.create(team=team, scoreboard=group_scoreboard)
        for bot_team in self.bot_teams:
            Row.objects.create(team=bot_team, scoreboard=group_scoreboard)

    def run_six_hour_tournament(self, match_map):
        segmentation = self._get_segmentation()
        for teams_of_a_match in segmentation:
            match = Match.objects.create(type=MatchTypes.DIFFERENT, group=self.group, map=match_map)
            self._create_match_teams(match, teams_of_a_match)
            self._create_games(match, teams_of_a_match)

    def permutations_for_single_match(self, teams, match_type=MatchTypes.DIFFERENT):
        if match_type == MatchTypes.SIMILAR:
            return [[teams[0], teams[0]], [teams[1], teams[1]]]
        return [[[teams[0], teams[1]], [teams[2], teams[3]]], [[teams[0], teams[2]], [teams[1], teams[3]]],
                [[teams[0], teams[3]], [teams[1], teams[2]]]]

    def _get_segmentation(self):
        segmentation = []
        if len(self.teams) % 4 != 0:
            for i in range(0, 4 - len(self.teams) % 4):
                self.teams.insert(-1 * (8 * i + 1), self.bot_teams[i])
        while len(self.teams) > 0:
            first_eight_teams = self.teams[:8]
            shuffle(first_eight_teams)
            selection = first_eight_teams[:4]
            self.teams = [team for team in self.teams if team not in selection]
            segmentation.append(selection)

        return segmentation

    def _create_match_teams(self, match, teams_of_a_match):
        match_teams = []
        for team in teams_of_a_match:
            match_teams.append(MatchTeam(team=team, match=match))
        MatchTeam.objects.bulk_create(match_teams)
        match.save()

    def _create_games(self, match, teams):
        permutations_of_match = self.permutations_for_single_match(teams)
        for permutation in permutations_of_match:
            game = Game.objects.create(match=match)
            self._create_game_side(game, permutation)
            game.save()
            self.games_ids.append(game.id)

    def _create_game_side(self, game, permutation):
        game_sides = []
        for side in permutation:
            game_side = GameSide.objects.create(game=game)
            for team_of_side in side:
                GameTeam.objects.create(team=team_of_side, game_side=game_side)
            game_sides.append(game_side)
        GameSide.objects.bulk_create(game_sides)
