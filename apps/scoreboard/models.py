from django.db import models

from polymorphic.models import PolymorphicModel


class ScoreBoardTypes:
    CHALLENGE = 'challenge'
    GROUP = 'group'
    FRIENDLY = 'friendly'


class Row(models.Model):
    team = models.ForeignKey('participation.Team', related_name='rows', on_delete=models.CASCADE)
    scoreboard = models.ForeignKey('ScoreBoard', related_name='rows', on_delete=models.CASCADE)
    score = models.FloatField(default=2000.0, db_index=True)
    rank = models.IntegerField(default=1)
    wins = models.IntegerField(default=0)
    loss = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)

    def __str__(self):
        return self.team.name


class ScoreBoard(PolymorphicModel):
    freeze = models.BooleanField(default=False)
    type = models.CharField(max_length=20, default=ScoreBoardTypes.CHALLENGE)


class ChallengeScoreBoard(ScoreBoard):
    challenge = models.OneToOneField('challenge.Challenge', related_name='scoreboard', on_delete=models.CASCADE)

    @staticmethod
    def get_scoreboard_sorted_rows(challenge):
        return ChallengeScoreBoard.objects.get(challenge=challenge).rows.all().order_by('-score')

    def pre_save(self):
        self.type = ScoreBoardTypes.CHALLENGE

    def save(self, *args, **kwargs):
        self.pre_save()
        super().save(*args, **kwargs)


class GroupScoreBoard(ScoreBoard):
    group = models.OneToOneField('challenge.Group', related_name='scoreboard', on_delete=models.CASCADE)
    calculated = models.BooleanField(default=False)

    @staticmethod
    def get_scoreboard_sorted_rows(group):
        return GroupScoreBoard.objects.get(group=group).rows.all().order_by('-score')

    def pre_save(self):
        self.type = ScoreBoardTypes.GROUP

    def save(self, *args, **kwargs):
        self.pre_save()
        super().save(*args, **kwargs)

    def __str__(self):
        return 'id: ' + str(self.id) + "  Tournament: " + self.group.stage.tournament.name + "  Group: " + str(
            self.group.id)


class FriendlyScoreBoard(ScoreBoard):
    pass

    def pre_save(self):
        self.type = ScoreBoardTypes.FRIENDLY

    def save(self, *args, **kwargs):
        self.pre_save()
        super().save(*args, **kwargs)
