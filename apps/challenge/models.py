import json
import logging
import os
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import ContentFile, File
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from polymorphic.models import PolymorphicModel

from apps.scoreboard.models import ChallengeScoreBoard, ScoreBoardTypes
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


class SingleGameStatusTypes:
    RUNNING = 'running'
    FAILED = 'failed'
    DONE = 'done'
    WAITING = 'waiting'
    WAITING_ACCEPT = 'waiting_accept'
    REJECTED = 'rejected'
    TYPES = (
        (RUNNING, _('Running')),
        (FAILED, _('Failed')),
        (DONE, _('Done')),
        (WAITING, _('Waiting')),
        (WAITING_ACCEPT, _('Waiting to accept')),
        (REJECTED, _('Rejected'))
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
    friendly_game_delay = models.IntegerField(default=5)
    code_submit_delay = models.IntegerField(default=5)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name + " type: " + self.type + " id: " + str(self.id)


class Tournament(PolymorphicModel):
    name = models.CharField(max_length=256)
    challenge = models.ForeignKey('challenge.Challenge', related_name='tournaments', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TournamentTypes.TYPES, default=TournamentTypes.HOURLY)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now_add=True)
    submit_deadline = models.DateTimeField(null=True, blank=True)
    queued = models.BooleanField(default=False)
    tournament_map = models.ForeignKey('challenge.Map', related_name='tournaments', on_delete=models.DO_NOTHING)
    match_bet_percentage = models.PositiveSmallIntegerField(default=5)

    def save(self, *args, **kwargs):
        self.queued = True
        if not self.tournament_map.verified:
            raise ValueError("Selected map not verified")
        super().save(*args, **kwargs)

    def __str__(self):
        return "challenge: " + self.challenge.__str__() + "\n" + "name: " \
               + self.name + " type: " + self.type + " id: " + str(
            self.id)

    @property
    def finished(self):
        for stage in self.stages.filter(finished=False):
            stage.check_finished()
        return self.stages.count() == self.stages.filter(finished=True).count()


class Stage(models.Model):
    tournament = models.ForeignKey('challenge.Tournament', related_name='stages', on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)

    def check_finished(self):
        for group in self.groups.all():
            if not group.finished:
                return False
        self.finished = True
        self.save()
        return True


class Group(models.Model):
    stage = models.ForeignKey('challenge.Stage', related_name='groups', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    @property
    def finished(self):
        return self.matches.count() == self.matches.filter(finished=True).count()


class GroupTeam(models.Model):
    team = models.ForeignKey('participation.Team', related_name='team_group', on_delete=models.CASCADE)
    group = models.ForeignKey('challenge.Group', related_name='team_groups', on_delete=models.CASCADE)


class Match(models.Model):
    group = models.ForeignKey('challenge.Group', related_name='matches', on_delete=models.CASCADE)
    map = models.ForeignKey('challenge.Map', related_name='matches', on_delete=None)
    type = models.CharField(max_length=64, choices=MatchTypes.TYPES)
    time = models.DateTimeField(auto_now_add=True, null=True)
    finished = models.BooleanField(default=False)

    def update_match_team_score(self, game_teams):
        games_done = self.games.filter(status=SingleGameStatusTypes.DONE).count()
        for game_team in game_teams:
            row = self.group.scoreboard.rows.get(team=game_team.team)
            game_side_id = GameTeam.objects.filter(team=game_team.team).filter(
                game_side__game=game_team.game_side.game).values_list('game_side_id', flat=True).get(
                game_side__game__match=self)
            game_side = GameSide.objects.get(id=game_side_id)
            print("Oomad match ro update koneeeeeeeeee :D\n ****************************************")
            print(game_side.game_teams.all().values_list('team__name', 'score', 'game_side__has_won'))
            if game_side.has_won:
                row.wins += 1
            elif game_side.game.game_sides.filter(has_won=False).count() == 2:
                row.draws += 1
            else:
                row.loss += 1
            row.save()
            match_team = self.match_teams.get(team=game_team.team)
            match_team.score += game_team.scoreboard_score
            match_team.save()
        if games_done >= 3:
            self.finished = True
            self.save()


class MatchTeam(models.Model):
    team = models.ForeignKey('participation.Team', related_name='game_team', on_delete=models.CASCADE)
    match = models.ForeignKey('challenge.Match', related_name='match_teams', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)


class Game(models.Model):
    match = models.ForeignKey('challenge.Match', related_name='games', on_delete=models.CASCADE, blank=True, null=True)
    infra_game_message = models.CharField(max_length=1023, null=True, blank=True)
    infra_token = models.CharField(max_length=256, null=True, blank=True, unique=True)
    status = models.CharField(max_length=50, choices=SingleGameStatusTypes.TYPES, default=SingleGameStatusTypes.WAITING)
    time = models.DateTimeField(auto_now_add=True, null=True)

    def get_log_file_directory(self, filename):
        return os.path.join('logs', 'single_game', self.infra_token if self.infra_token else str(self.id), filename)

    log = models.FileField(upload_to=get_log_file_directory, blank=True, null=True)

    @property
    def is_friendly(self):
        return self.match is None

    def update_scores_and_client_logs(self, client0_log, client0_log_name, client1_log, client1_log_name, client2_log,
                                      client2_log_name, client3_log, client3_log_name):
        from apps.challenge.services.utils import update_game_team_scoreboard_score

        score = json.loads(self.log.read()).get('end')
        score = sorted(score, key=lambda x: x['playerId'])
        client0 = self.game_sides.all().order_by('id')[0].game_teams.all().order_by('id')[0]
        client1 = self.game_sides.all().order_by('id')[1].game_teams.all().order_by('id')[0]
        client2 = self.game_sides.all().order_by('id')[0].game_teams.all().order_by('id')[1]
        client3 = self.game_sides.all().order_by('id')[1].game_teams.all().order_by('id')[1]
        client0.save_client_log(filename=client0_log_name + ".zip", response=client0_log)
        client1.save_client_log(filename=client1_log_name + ".zip", response=client1_log)
        client2.save_client_log(filename=client2_log_name + ".zip", response=client2_log)
        client3.save_client_log(filename=client3_log_name + ".zip", response=client3_log)
        client0.score = score[0]['score']
        client2.score = score[2]['score']
        client1.score = score[1]['score']
        client3.score = score[3]['score']
        if score[0]['score'] + score[2]['score'] > score[1]['score'] + score[3]['score']:
            game_side = self.game_sides.all().order_by('id')[0]
            game_side.has_won = True
            game_side.save()
        elif score[0]['score'] + score[2]['score'] < score[1]['score'] + score[3]['score']:
            game_side = self.game_sides.all().order_by('id')[1]
            game_side.has_won = True
            game_side.save()
        client0.save()
        client1.save()
        client2.save()
        client3.save()
        if self.match:
            update_game_team_scoreboard_score(self, self.match.group.scoreboard)
            self.match.update_match_team_score([client0, client1, client2, client3])
        else:
            self._update_friendly_scoreboard([client0, client1, client2, client3])

    @property
    def winner_side(self):
        if self.game_sides.all().order_by('id')[0].has_won:
            return 1
        elif self.game_sides.all().order_by('id')[1].has_won:
            return 2
        else:
            return 0

    def _update_friendly_scoreboard(self, game_teams):
        from apps.scoreboard.models import ScoreBoard
        from apps.challenge.services.stats import Stats
        from apps.challenge.services.utils import update_game_team_scoreboard_score
        friendly_scoreboard = ScoreBoard.objects.get(type=ScoreBoardTypes.FRIENDLY)
        update_game_team_scoreboard_score(game=self, scoreboard=friendly_scoreboard)
        for game_team in game_teams:
            row = friendly_scoreboard.rows.get(team=game_team.team)
            # row.score += game_team.score
            row.wins, row.draws, row.loss = Stats(team=game_team.team, friendly_only=True)()
            row.save()

    def __str__(self):
        return "infra_token: " + (self.infra_token or 'None') + " status: " + self.status + " id: " + str(self.id)


class GameSide(models.Model):
    game = models.ForeignKey('challenge.Game', related_name='game_sides', on_delete=models.CASCADE)
    has_won = models.BooleanField(default=False)

    def __str__(self):
        return "id: " + str(self.id)


class GameTeam(models.Model):
    team = models.ForeignKey('participation.Team', related_name='game_teams', on_delete=models.CASCADE)
    game_side = models.ForeignKey('challenge.GameSide', related_name='game_teams', on_delete=models.CASCADE)

    def team_single_game_log(self, filename):
        return os.path.join('logs', 'just_team', self.team.name, self.game_side.game.infra_token, filename)

    log = models.FileField(upload_to=team_single_game_log, null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    scoreboard_score = models.FloatField(default=0.0)

    def save_client_log(self, filename, response):
        with open(filename, 'wb') as f:
            for chunk in response:
                f.write(chunk)
        f = open(filename, 'rb')
        self.log.save(name=filename, content=File(f))
        f.close()
        os.remove(filename)

    def __str__(self):
        return "team: " + self.team.__str__() + "\n" + " id: " + str(self.id)


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
        return "id: " + str(self.id) + ' team: ' + self.team.name + " user: " + self.user.username

    def set_final(self):
        """
            Use this method instead of changing the is_final attribute directly
            This makes sure that only one instance of TeamSubmission has is_final flag set to True
        """
        if self.status != 'compiled':
            raise ValueError(_('This submission is not compiled yet.'))
        Submission.objects.filter(is_final=True, team=self.team).update(is_final=False)
        self.is_final = True
        self.save()

    def handle(self):
        # handle_submission(self.id)
        handle_submission.delay(self.id)

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
    time_created = models.DateTimeField(auto_now_add=True)
    verified = models.NullBooleanField(null=True, blank=True)

    def map_directory_path(self, filename):
        return os.path.join('maps', self.name, filename)

    file = models.FileField(blank=True, null=True, upload_to=map_directory_path)

    def pre_save(self):
        from . import functions
        self.infra_token = functions.upload_file(self.file)

    def save(self, *args, **kwargs):
        self.pre_save()
        super().save(*args, **kwargs)


class Lobby(models.Model):
    teams1 = models.ManyToManyField('participation.Team', related_name='lobbies1', null=True, blank=True)
    teams2 = models.ManyToManyField('participation.Team', related_name='lobbies2', null=True, blank=True)
    match = models.ForeignKey('challenge.Match', related_name='friendly_matches', on_delete=models.CASCADE, null=True,
                              blank=True)
    completed = models.BooleanField(default=False)
    multi_play = models.BooleanField(default=False)
    with_friend = models.BooleanField(default=True)
