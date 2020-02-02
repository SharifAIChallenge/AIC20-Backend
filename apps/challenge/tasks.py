from random import random

from celery.schedules import crontab
from celery.task import periodic_task

from apps.challenge.models import Info, Game
from thebackend.celery import app
from .models import MatchTypes, Match


@app.task('run_single_game')
def run_single_game(match):
    info = Info(status="pending", detail="")
    info.save()
    game = Game(match=match, info=info)
    game.save()
    # TODO: send request to infra here
    return game


def random_four_numbers(max_number):
    list_of_random_number = []
    count_of_random_number = 0
    while count_of_random_number < 4:
        random_number = (random() * max_number)
        if random_number not in list_of_random_number:
            list_of_random_number.append(random_number)
            count_of_random_number += 1
    return list_of_random_number


def permutations_for_single_games(match_type=MatchTypes.DIFFERENT):
    if match_type == MatchTypes.SIMILAR:
        return [[1, 1, 2, 2]]
    return [[1, 2, 3, 4], [1, 3, 2, 4], [1, 4, 2, 3]]


def six_hour_tournament_segmentation_teams(teams: list):
    teams_segmentation = []
    while len(teams) >= 4:
        selected_teams_index = random_four_numbers(max(8, len(teams)))  # 4 random number between 0 to (7 or len)
        teams_segmentation.append([teams.pop(index) for index in selected_teams_index])
    if len(teams) > 0:
        for i in range(4 - len(teams)):
            teams.append(None)
        teams_segmentation.append(teams)
    return teams_segmentation


def create_match_from_list_of_teams(match_teams):
    for teams_of_a_match in match_teams:
        pass


