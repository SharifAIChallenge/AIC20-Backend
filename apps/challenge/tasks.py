from random import random

from apps.challenge.models import Info, Game, MatchTeam, GameTeam, GameSide
from thebackend.celery import app
from .models import MatchTypes, Match


@app.task(name='handle_submission')
def handle_submission(submission_id):
    from .models import Submission

    submission = Submission.objects.get(id=submission_id)
    try:
        submission.upload()
        submission.compile()

    except Exception as error:
        logger.error(error)

# def random_four_numbers(max_number):
#     list_of_random_number = []
#     count_of_random_number = 0
#     while count_of_random_number < 4:
#         random_number = (random() * max_number)
#         if random_number not in list_of_random_number:
#             list_of_random_number.append(random_number)
#             count_of_random_number += 1
#     return list_of_random_number
#
#
# def permutations_for_single_match(match_type=MatchTypes.DIFFERENT):
#     if match_type == MatchTypes.SIMILAR:
#         return [[1, 1], [2, 2]]
#     return [[1, 2], [3, 4], [1, 3], [2, 4], [1, 4], [2, 3]]
#
#
# def six_hour_tournament_segmentation_teams(teams: list):
#     teams_segmentation = []
#     while len(teams) >= 4:
#         selected_teams_index = random_four_numbers(max(8, len(teams)))
#         teams_segmentation.append([teams.pop(index) for index in selected_teams_index])
#     if len(teams) > 0:
#         for i in range(4 - len(teams)):
#             teams.append(None)
#         teams_segmentation.append(teams)
#     return teams_segmentation
#
#
# def run_six_hour_tournament(teams, group, match_map):
#     match_teams = six_hour_tournament_segmentation_teams(teams)
#     for teams_of_a_match in match_teams:
#         match = Match(type=MatchTypes.DIFFERENT, group=group, map=match_map)
#         create_match(match, teams_of_a_match)
#         create_games(match)
#
#
# def create_games(match):
#     permutations_of_match = permutations_for_single_match()
#     for permutation in permutations_of_match:
#         info = Info.objects.create(status="pending", detail="")
#         game = Game(match=match, info=info)
#         create_game_side(game, permutation)
#         game.save()
#
#
# def create_game_side(game, permutation):
#     game_sides = []
#     for side in permutation:
#         game_side = GameSide(game=game)
#         for team_of_side in side:
#             GameTeam.objects.create(team=team_of_side, game_side=game_side)
#         game_sides.append(game_side)
#     GameSide.objects.bulk_create(game_sides)
#
#
# def create_match(match, teams_of_a_match):
#     match_teams = []
#     for team in teams_of_a_match:
#         match_teams.append(MatchTeam(team=team, match=match))
#     MatchTeam.objects.bulk_create(match_teams)
#     match.save()
