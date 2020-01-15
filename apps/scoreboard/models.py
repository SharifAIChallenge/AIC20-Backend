from django.db import models


# Create your models here.


class Row(models.Model):
    team = models.ForeignKey('participation.Participant', related_name='rows', on_delete=models.CASCADE)
    scoreboard = models.ForeignKey('scoreboard.ScoreBoard', related_name='rows', on_delete=models.CASCADE)


class Score(models.Model):
    row = models.OneToOneField('scoreboard.Row', related_name='score', on_delete=models.CASCADE)
    number = models.FloatField(default=1000.0)


class ScoreBoard(models.Model):
    tournament = models.ForeignKey('challenge.Tournament', related_name='scoreboards', on_delete=models.CASCADE)
    stage = models.OneToOneField('challenge.Stage', related_name='scoreboard', on_delete=models.CASCADE)
