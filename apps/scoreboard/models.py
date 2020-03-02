from django.db import models

from polymorphic.models import PolymorphicModel


class Row(models.Model):
    team = models.ForeignKey('participation.Team', related_name='rows', on_delete=models.CASCADE)
    scoreboard = models.ForeignKey('ScoreBoard', related_name='rows', on_delete=models.CASCADE)
    score = models.FloatField(default=1000.0)
    rank = models.IntegerField(default=1)
    wins = models.IntegerField(default=0)
    loss = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)

    def __str__(self):
        return self.team.name


class ScoreBoard(PolymorphicModel):
    freeze = models.BooleanField(default=False)


class ChallengeScoreBoard(ScoreBoard):
    challenge = models.OneToOneField('challenge.Challenge', related_name='scoreboard', on_delete=models.CASCADE)

    @staticmethod
    def get_scoreboard_sorted_rows(challenge):
        return ChallengeScoreBoard.objects.get(challenge=challenge).rows.all().order_by('-score')


class GroupScoreBoard(ScoreBoard):
    group = models.OneToOneField('challenge.Group', related_name='scoreboard', on_delete=models.CASCADE)
    calculated = models.BooleanField(default=False)

    @staticmethod
    def get_scoreboard_sorted_rows(group):
        return GroupScoreBoard.objects.get(group=group).rows.all().order_by('-score')


class FriendlyScoreBoard(ScoreBoard):
    pass
