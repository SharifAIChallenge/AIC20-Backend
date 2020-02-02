from random import random

from apps.challenge.models import Info, Game
from thebackend.celery import app
from .models import MatchTypes


@app.task('run_single_game')
def run_single_game(match):
    info = Info(status="pending", detail="")
    info.save()
    game = Game(match=match, info=info)
    game.save()
    # TODO: send request to infra here
    return game


def random_four_numbers():
    list_of_random_number = []
    count_of_random_number = 0
    while count_of_random_number < 4:
        random_number = (random() * 8) + 1
        if random_number not in list_of_random_number:
            list_of_random_number.append(random_number)
            count_of_random_number += 1
    return list_of_random_number


def permutations_for_single_games(match_type=MatchTypes.DIFFERENT):
    if match_type == MatchTypes.SIMILAR:
        return [[1, 1, 2, 2]]
    return [[1, 2, 3, 4], [1, 3, 2, 4], [1, 4, 2, 3]]


def six_hour_tournament():
    pass
