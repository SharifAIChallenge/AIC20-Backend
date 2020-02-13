import logging
import os
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from polymorphic.models import PolymorphicModel

from .tasks import handle_submission

logger = logging.getLogger(__name__)


# Create your models here.

class ChallengeTypes:
    PRIMARY = 'primary'
    FINAL = 'final'
    TYPES = (
        (PRIMARY, 'Primary Challenge'),
        (FINAL, 'Finale Challenge'),
    )


class TournamentTypes:
    LEAGUE = 'league'
    HOURLY = 'hourly'
    DOUBLE_ELIMINATION = 'double elimination'
    TYPES = (
        (LEAGUE, 'league'),
        (HOURLY, 'hourly'),
        (DOUBLE_ELIMINATION, 'double elimination')
    )


class MatchTypes:
    SIMILAR = "similar"
    DIFFERENT = "different"
    TYPES = (
        (SIMILAR, 'Similar Teams'),
        (DIFFERENT, 'Different Teams'),
    )


class SubmissionLanguagesTypes:
    CPP = 'cpp'
    JAVA = 'java'
    PYTHON3 = 'py3'
    GO = 'go'

    TYPES = (
        (CPP, _('C++')),
        (JAVA, _('Java')),
        (PYTHON3, _('Python 3')),
        (GO, _('Go'))
    )


class SubmissionStatusTypes:
    UPLOADING = 'uploading'
    UPLOADED = 'uploaded'
    COMPILING = 'compiling'
    COMPILED = 'compiled'
    FAILED = 'failed'

    TYPES = (
        (UPLOADING, _('Uploading')),
        (UPLOADED, _('Uploaded')),
        (COMPILING, _('Compiling')),
        (COMPILED, _('Compiled')),
        (FAILED, _('Failed'))
    )


class Challenge(models.Model):
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=50, choices=ChallengeTypes.TYPES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class Tournament(PolymorphicModel):
    challenge = models.ForeignKey('challenge.Challenge', related_name='tournaments', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TournamentTypes.TYPES)
    start_time = models.DateTimeField()
    submit_deadline = models.DateTimeField()


class Stage(models.Model):
    tournament = models.ForeignKey('challenge.Tournament', related_name='stages', on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)


class Group(models.Model):
    stage = models.ForeignKey('challenge.Stage', related_name='groups', on_delete=models.CASCADE)


class TeamGroup(models.Model):
    team = models.ForeignKey('participation.Team', related_name='team_group', on_delete=models.CASCADE)
    group = models.ForeignKey('challenge.Group', related_name='team_groups', on_delete=models.CASCADE)


class Match(models.Model):
    group = models.ForeignKey('challenge.Group', related_name='matches', on_delete=models.CASCADE)
    map = models.ForeignKey('challenge.Map', related_name='matches', on_delete=None)
    type = models.CharField(max_length=64, choices=MatchTypes.TYPES)


class MatchTeam(models.Model):
    team = models.ForeignKey('participation.Team', related_name='game_team', on_delete=models.CASCADE)
    match = models.ForeignKey('challenge.Match', related_name='match_teams', on_delete=models.CASCADE)


class Game(models.Model):
    match = models.ForeignKey('challenge.Match', related_name='games', on_delete=models.CASCADE)
    info = models.OneToOneField('challenge.Info', related_name='game', on_delete=models.CASCADE, null=True)


class GameSide(models.Model):
    game = models.ForeignKey('challenge.Game', related_name='game_sides', on_delete=models.CASCADE)
    has_won = models.BooleanField(default=False)


class GameTeam(models.Model):
    team = models.ForeignKey('participation.Team', related_name='game_teams', on_delete=models.CASCADE)
    game_side = models.ForeignKey('challenge.GameSide', related_name='game_teams', on_delete=models.CASCADE)


class Info(models.Model):
    status = models.CharField(max_length=50)
    detail = models.CharField(max_length=500)


def get_submission_file_directory(instance, filename):
    return os.path.join(instance.team.name, str(instance.user.id), filename + uuid.uuid4().__str__() + '.zip')


class Submission(models.Model):
    FILE_SIZE_LIMIT = 20 * 1024 * 1024

    team = models.ForeignKey('participation.Team', related_name='submissions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='submissions', on_delete=models.CASCADE)
    language = models.CharField(max_length=50, choices=SubmissionLanguagesTypes.TYPES,
                                default=SubmissionLanguagesTypes.JAVA)
    file = models.FileField(upload_to=get_submission_file_directory)
    submit_time = models.DateTimeField(auto_now_add=True)
    is_final = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=SubmissionStatusTypes.TYPES,
                              default=SubmissionStatusTypes.UPLOADING)
    infra_compile_message = models.CharField(max_length=1023, null=True, blank=True)
    infra_token = models.CharField(max_length=256, null=True, blank=True, unique=True)
    infra_compile_token = models.CharField(max_length=256, null=True, blank=True, unique=True)

    def __str__(self):
        return str(self.id) + ' team: ' + str(self.team) + ' is final: ' + str(self.is_final)

    def set_final(self):
        """
            Use this method instead of changing the is_final attribute directly
            This makes sure that only one instance of TeamSubmission has is_final flag set to True
        """
        # if self.status != 'compiled':
        #     raise ValueError(_('This submission is not compiled yet.'))
        Submission.objects.filter(is_final=True, team=self.team).update(is_final=False)
        self.is_final = True
        self.save()

    def handle(self):
        handle_submission(self.id)
        # handle_submission.delay(self.id)

    def upload(self):
        from . import functions
        self.infra_token = functions.upload_file(self.file)
        self.status = SubmissionStatusTypes.UPLOADED
        self.save()

    def compile(self):
        from . import functions
        result = functions.compile_submissions([self])
        if result[0]['success']:
            self.status = SubmissionStatusTypes.COMPILING
            self.infra_compile_token = result[0]['run_id']
        else:
            logger.error(result[0][self.infra_token]['errors'])
        self.save()


class Map(models.Model):
    name = models.CharField(max_length=128)
    infra_token = models.CharField(max_length=256, null=True, blank=False, unique=True)
