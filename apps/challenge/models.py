from django.db import models

from polymorphic.models import PolymorphicModel


# Create your models here.

class TournamentTypes:
    LEAGUE = 'league'
    HOURLY = 'hourly'
    DOUBLE_ELIMINATION = 'double elimination'
    TYPES = (
        (LEAGUE, 'league'),
        (HOURLY, 'hourly'),
        (DOUBLE_ELIMINATION, 'double elimination')
    )


class Challenge(models.Model):
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class Tournament(PolymorphicModel):
    type = models.CharField(max_length=20, choices=TournamentTypes.TYPES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    run_time = models.DateTimeField()


class Stage(models.Model):
    pass


class Groups(models.Model):
    pass


class Match(models.Model):
    pass


class MatchTeam(models.Model):
    pass


class Game(models.Model):
    pass


class GameSide(models.Model):
    pass


class GameTeam(models.Model):
    pass


class Info(models.Model):
    pass


class Submission(models.Model):
    pass
