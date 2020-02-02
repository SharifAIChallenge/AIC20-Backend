from django.db import models

from polymorphic.models import PolymorphicModel


class Row(models.Model):
    team = models.ForeignKey('participation.Participant', related_name='rows', on_delete=models.CASCADE)
    scoreboard = models.ForeignKey('scoreboard.ScoreBoard', related_name='rows', on_delete=models.CASCADE)
    score = models.FloatField(default=1000.0)


class ScoreBoard(PolymorphicModel):
    freeze = models.BooleanField(default=False)


class ChallengeScoreBoard(ScoreBoard):
    challenge = models.OneToOneField('challenge.Challenge', related_name='scoreboard', on_delete=models.CASCADE)


class GroupScoreBoard(ScoreBoard):
    group = models.OneToOneField('challenge.Group', related_name='scoreboard', on_delete=models.CASCADE)
