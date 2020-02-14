import logging

from random import random

from thebackend.celery import app

# from .models import MatchTypes, Match

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
