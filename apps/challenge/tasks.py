import logging

from random import random

from thebackend.celery import app

logger = logging.getLogger(__name__)


@app.task(name='handle_submission')
def handle_submission(submission_id):
    from .models import Submission

    submission = Submission.objects.get(id=submission_id)
    try:
        submission.upload()
        submission.compile()

    except Exception as error:
        logger.error(error)


@app.task(name='hourly_tournament')
def hourly_tournament(tournament_id):
    from .services.tournament_creator import TournamentCreator
    from .models import TournamentTypes, Tournament
    tournament = Tournament.objects.get(id=tournament_id)
    tournament_creator = TournamentCreator(tournament=tournament)
    group = tournament_creator()

    game_ids = []
    for match in group.matches.all():
        for game in match.games.all():
            game_ids.append(game)
    run_game.delay(game_ids)


@app.task(name='run_game')
def run_game(game_ids):
    from .models import Game
    from .functions import run_games
    single_games = Game.objects.filter(id__in=game_ids)
    run_games(single_games=single_games)


@app.task(name='run_friendly_game')
def run_friendly_game(game_id):
    from .models import FriendlyGame
    from .functions import run_games
    friendly_game = FriendlyGame.objects.get(id=game_id)
    run_games([friendly_game])
