import logging

from random import random

from thebackend.celery import app

logger = logging.getLogger(__name__)


@app.task(name='handle_submission')
def handle_submission(submission_id):
    from .models import Submission
    print("ommad too task")
    submission = Submission.objects.get(id=submission_id)
    try:
        if not submission.infra_token:
            submission.upload()
        submission.compile()

    except Exception as error:
        logger.error(error)


@app.task(name='run_single_game')
def run_single_game(game_id, game_map_id=None):
    from .models import Game, SingleGameStatusTypes, Map
    from .functions import run_games
    single_game = Game.objects.get(id=game_id)
    game_map = Map.objects.get(id=game_map_id) if game_map_id else None
    response = run_games(single_games=[single_game], desired_map=game_map)[0]
    if response['success']:
        single_game.infra_token = response['run_id']
        single_game.status = SingleGameStatusTypes.RUNNING
    else:
        single_game.status = SingleGameStatusTypes.FAILED
    single_game.save()


@app.task(name='run_multi_games')
def run_multi_games(game_ids):
    from .models import Game
    from .functions import run_games
    single_games = Game.objects.filter(id__in=game_ids)
    run_games(single_games=single_games)
