from random import random

from django.utils import timezone

from apps.challenge.tasks import create_game_side
from apps.scoreboard.models import ChallengeScoreBoard
from ..models import Challenge, Tournament, TournamentTypes, Stage, Group, GroupTeam, Match, MatchTeam, MatchTypes, \
    Info, Game, GameSide, GameTeam


class TournamentCreator:

    def __init__(self, challenge, start_time, submit_deadline, match_map, tournament_type=TournamentTypes.HOURLY):
        self.challenge = challenge
        self.score_board: ChallengeScoreBoard = ChallengeScoreBoard.objects.get(challenge=challenge)
        self.teams = self.score_board.rows.values_list('team', flat=True)
        self.start_time = start_time
        self.submit_deadline = submit_deadline
        self.match_map = match_map
        self.tournament_type = tournament_type
        self.tournament = ''
        self.stage = ''
        self.group = ''
        pass

    def __call__(self):
        self._create_tournament()
        self._create_stages()
        self._create_groups()
        self.run_six_hour_tournament(teams=self.teams, group=self.group, match_map=self.match_map)

    def _create_tournament(self):
        self.tournament = Tournament.objects.create(challenge=self.challenge, type=self.tournament_type,
                                                    end_time=self.submit_deadline)

    def _create_stages(self):
        self.stage = Stage.objects.create(tournament=self.tournament)

    def _create_groups(self):
        self.group = Group.objects.create(stage=self.stage)

    def random_four_numbers(self, max_number):
        list_of_random_number = []
        count_of_random_number = 0
        while count_of_random_number < 4:
            random_number = (random() * max_number)
            if random_number not in list_of_random_number:
                list_of_random_number.append(random_number)
                count_of_random_number += 1
        return list_of_random_number

    def permutations_for_single_match(self, teams, match_type=MatchTypes.DIFFERENT):
        if match_type == MatchTypes.SIMILAR:
            return [[teams[0], teams[0]], [teams[1], teams[1]]]
        return [[[teams[0], teams[1]], [teams[2], teams[3]]], [[teams[0], teams[2]], [teams[1], teams[3]]],
                [[teams[0], teams[3]], [teams[1], teams[2]]]]

    def six_hour_tournament_segmentation_teams(self, teams: list):
        teams_segmentation = []
        while len(teams) >= 4:
            selected_teams_index = self.random_four_numbers(max(8, len(teams)))
            teams_segmentation.append([teams.pop(index) for index in selected_teams_index])
        if len(teams) > 0:
            for i in range(4 - len(teams)):
                teams.append(None)
            teams_segmentation.append(teams)
        return teams_segmentation

    def run_six_hour_tournament(self, teams, group, match_map):
        match_teams = self.six_hour_tournament_segmentation_teams(teams)
        for teams_of_a_match in match_teams:
            match = Match(type=MatchTypes.DIFFERENT, group=group, map=match_map)
            self.create_match(match, teams_of_a_match)
            self.create_games(match)

    def create_games(self, match):
        permutations_of_match = self.permutations_for_single_match(match.match_teams.values_list('team', flat=True))
        for permutation in permutations_of_match:
            info = Info.objects.create(status="pending", detail="")
            game = Game(match=match, info=info)
            create_game_side(game, permutation)
            game.save()

    def create_game_side(self, game, permutation):
        game_sides = []
        for side in permutation:
            game_side = GameSide(game=game)
            for team_of_side in side:
                GameTeam.objects.create(team=team_of_side, game_side=game_side)
            game_sides.append(game_side)
        GameSide.objects.bulk_create(game_sides)

    def create_match(self, match, teams_of_a_match):
        match_teams = []
        for team in teams_of_a_match:
            match_teams.append(MatchTeam(team=team, match=match))
        MatchTeam.objects.bulk_create(match_teams)
        match.save()
