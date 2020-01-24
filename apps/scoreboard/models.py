from django.db import models


# Create your models here.


class Row(models.Model):
    team = models.ForeignKey('participation.Team', related_name='rows', on_delete=models.CASCADE)
    scoreboard = models.ForeignKey('scoreboard.ScoreBoard', related_name='rows', on_delete=models.CASCADE)
    score = models.FloatField(default=1000.0)


class ScoreBoard(models.Model):
    tournament = models.ForeignKey('challenge.Tournament', related_name='scoreboards', on_delete=models.CASCADE)
