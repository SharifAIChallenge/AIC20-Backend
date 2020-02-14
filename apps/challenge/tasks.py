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
def hourly_tournament():
    from .services.tournament_creator import TournamentCreator
    tournament_creator = TournamentCreator()
    pass
