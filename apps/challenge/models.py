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
    tournament = models.ForeignKey('challenge.Tournament', related_name='stages', on_delete=models.CASCADE)


class Group(models.Model):
    scoreboard = models.OneToOneField('scoreboard.Score', related_name='group', on_delete=None)


class TeamGroup(models.Model):
    team = models.OneToOneField('participation.Team', related_name='team_group', on_delete=models.CASCADE)
    group = models.ForeignKey('challenge.Group', related_name='team_groups', on_delete=models.CASCADE)


class Match(models.Model):
    pass


class MatchTeam(models.Model):
    team = models.OneToOneField('participation.Team', related_name='game_team', on_delete=models.CASCADE)
    match = models.ForeignKey('challenge.Match', related_name='match_teams', on_delete=models.CASCADE)


class Game(models.Model):
    pass


class GameSide(models.Model):
    game = models.ForeignKey('challenge.Game', related_name='game_sides', on_delete=models.CASCADE)


class GameTeam(models.Model):
    team = models.OneToOneField('participation.Team', related_name='game_team', on_delete=models.CASCADE)
    game_side = models.ForeignKey('challenge.GameSide', related_name='game_teams', on_delete=models.CASCADE)


class Info(models.Model):
    pass


class Submission(models.Model):
    pass
