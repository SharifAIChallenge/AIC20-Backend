from django.db import models

from polymorphic.models import PolymorphicModel


class Row(models.Model):
    team = models.ForeignKey('participation.Team', related_name='rows', on_delete=models.CASCADE)
    scoreboard = models.ForeignKey('scoreboard.ScoreBoard', related_name='rows', on_delete=models.CASCADE)
    score = models.IntegerField(default=1000)
    wins = models.IntegerField(default=0)
    loss = models.IntegerField(default=0)


class ScoreBoard(PolymorphicModel):
    freeze = models.BooleanField(default=False)


class ChallengeScoreBoard(ScoreBoard):
    challenge = models.OneToOneField('challenge.Challenge', related_name='scoreboard', on_delete=models.CASCADE)

    @staticmethod
    def get_scoreboard_sorted_rows(challenge):
        return ChallengeScoreBoard.objects.get(challenge=challenge).rows.all().order_by('-score')


class GroupScoreBoard(ScoreBoard):
    group = models.OneToOneField('challenge.Group', related_name='scoreboard', on_delete=models.CASCADE)

    @staticmethod
    def get_scoreboard_sorted_rows(group):
        return GroupScoreBoard.objects.get(group=group).rows.all().order_by('-score')
