from itertools import combinations

from apps.challenge.models import Submission, Group, Stage, GroupTeam, MatchTeam, MatchTypes, Match, Game, GameSide
from apps.participation.models import Team
from apps.scoreboard.models import ChallengeScoreBoard, GroupScoreBoard, Row


class LeagueCreator:

    def __init__(self, tournament):
        self.rows = ChallengeScoreBoard.get_scoreboard_sorted_rows(tournament.challenge)
        self.teams = []
        self.bot_teams = []
        self.tournament = tournament
        self.group_scoreboards = []
        self.stage = ''
        self.seeds = []
        self.group_teams_separated_by_groups = []
        self.groups = []
        self.games_ids = []

    def __call__(self, *args, **kwargs):
        self._get_bot_teams()
        self._filter_teams()
        self._create_stages()
        self._create_seeds()
        self._create_groups()
        self._create_league(self.tournament.tournament_maps.all())
        return self.games_ids

    def _get_bot_teams(self):
        self.bot_teams.extend(Team.objects.filter(name__in=['ufo1', 'ufo2', 'ufo3', 'ufo4']))

    def _filter_teams(self):
        filtered_teams = []
        for row in self.rows:
            if Submission.objects.filter(team=row.team).filter(
                    is_final=True).exists() and row.team.name not in ['ufo1', 'ufo2', 'ufo3', 'ufo4']:
                filtered_teams.append(row.team)
        self.teams = filtered_teams

    def _create_stages(self):
        self.stage = Stage.objects.create(tournament=self.tournament)

    def _create_seeds(self):
        self.seeds = [self.teams[12 * i: 12 * i + 12] for i in range(len(self.teams) // 12)]

    def _create_groups(self):
        for i in range(len(self.seeds[0])):
            group = Group.objects.create(stage=self.stage)
            group_teams = [GroupTeam(group=group, team=seed[i]) for seed in self.seeds]
            GroupTeam.objects.bulk_create(group_teams)
            self.group_scoreboard = group_scoreboard = GroupScoreBoard.objects.create(group=group)
            for group_team in group_teams:
                Row.objects.create(team=group_team.team, scoreboard=group_scoreboard)
            self.groups.append(group)
            self.group_teams_separated_by_groups.append(group_teams)

    def _create_league(self, match_maps):
        for match_map in match_maps:
            for group_teams in self.group_teams_separated_by_groups:
                segmentation = self._get_segmentation([group_team.team for group_team in group_teams])
                for teams_of_a_match in segmentation:
                    match = Match.objects.create(type=MatchTypes.DIFFERENT, group=group_teams[0].group, map=match_map)
                    self._create_match_teams(match, teams_of_a_match)
                    self._create_games(match, teams_of_a_match)

    def _get_segmentation(self, teams):
        return list(combinations(teams, 4))

    def permutations_for_single_match(self, teams, match_type=MatchTypes.DIFFERENT):
        if match_type == MatchTypes.SIMILAR:
            return [[teams[0], teams[0]], [teams[1], teams[1]]]
        return [[[teams[0], teams[1]], [teams[3], teams[2]]], [[teams[0], teams[2]], [teams[1], teams[3]]],
                [[teams[0], teams[3]], [teams[2], teams[1]]]]

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
