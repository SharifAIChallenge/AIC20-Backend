import json
from datetime import datetime, timedelta

from django.db import transaction
from django.db.models import Q
from django.utils.timezone import utc
from rest_framework.generics import get_object_or_404

from apps.challenge.models import Lobby, Challenge, ChallengeTypes, Submission
from apps.challenge.models import Game, GameSide, GameTeam
from apps.participation.models import Team


class FriendlyGameTypes:
    SINGLE = 'single'
    MULTI = 'multi'


class MultiFriendlyGameTypes:
    FRIEND = 'friend'
    ENEMY = 'enemy'


class FriendlyGameCreator:

    def __init__(self, lobby):
        self.lobby = lobby
        self.friendly_game = ''
        self.friendly_game_teams = []
        self.friendly_game_sides = []

    def __call__(self, *args, **kwargs):
        self._create_friendly_game()
        self._create_friendly_game_teams()
        return self.friendly_game

    def _create_friendly_game(self):
        self.friendly_game = Game.objects.create()
        self.lobby.game = self.friendly_game
        self.lobby.save()

    def _create_game_sides(self):
        for _ in range(2):
            self.friendly_game_sides.append(GameSide.objects.create(game=self.friendly_game))

    def _create_friendly_game_teams(self):
        for team in self.lobby.teams1.all():
            self.friendly_game_teams.append(
                GameTeam.objects.create(team=team, game_side=self.friendly_game_sides[0]))
        for team in self.lobby.teams2.all():
            self.friendly_game_teams.append(
                GameTeam.objects.create(team=team, game_side=self.friendly_game_sides[1])
            )


class LobbyHandler:

    def __init__(self, request):
        self.request = request
        self.data = json.loads(request.body)
        self.type = ''
        self.multi_type = ''
        self.team_name = ''
        self.team = None
        self.lobby = None
        self.errors = []
        self.friendly_game = None
        self.valid = True
        self.test = ''

    def __call__(self):
        self._validate_friendly_delay()
        if self.valid:
            self._set_type()
        if self.valid and self.type == FriendlyGameTypes.MULTI:
            self._set_multi_type()
            self._set_team()
        if self.valid:
            self._validate_teams()
        if self.valid:
            self._handle_lobby()
        if self.valid and self.lobby.completed:
            self.friendly_game = FriendlyGameCreator(lobby=self.lobby)

        return self.errors, self.friendly_game, self.test

    def _validate_friendly_delay(self):
        challenge = Challenge.objects.get(type=ChallengeTypes.PRIMARY)
        last_friendly_game = GameTeam.objects.filter(team=self.request.user.participant.team).filter(
            game_side__game__match=None).order_by('game_side__game__time').values_list('game_side__game',
                                                                                       flat=True).last()
        if last_friendly_game and datetime.now(utc) - last_friendly_game.time < timedelta(
                minutes=challenge.friendly_game_delay):
            self.valid = False
            self.errors.append(
                f"pleaseWait")

    def _set_type(self):
        self.type = self.data.get('type', FriendlyGameTypes.SINGLE)

    def _set_multi_type(self):
        self.multi_type = self.data.get('multi_type', MultiFriendlyGameTypes.FRIEND)

    def _set_team(self):
        self.team_name = self.data.get('team_name')
        if self.multi_type == FriendlyGameTypes.MULTI and not self.team_name:
            self.valid = False
            self.errors.append("provideTeamName")
            return
        if self.team_name == self.request.user.participant.team.name:
            self.valid = False
            self.errors.append("cantInviteYourself")
            return
        self.team = get_object_or_404(Team, name=self.team_name)
        if not self.team.allow_multi_friendly:
            self.valid = False
            self.errors.append("doesntAcceptInvitation")
        if not self.request.user.participant.team.allow_multi_friendly:
            self.valid = False
            self.errors.append("pleaseEnableInvitation")

    def _validate_teams(self):
        if not self.request.user.participant.team.is_valid:
            self.valid = False
            self.errors.append("teamInvalid")
            return
        if not Submission.objects.filter(team=self.request.user.participant.team).filter(is_final=True).exists():
            self.valid = False
            self.errors.append("teamHasNoFinalSubmission")
        if self.team and not self.team.is_valid:
            self.valid = False
            self.errors.append("invitedTeamInvalid")
            return
        if self.team and not Submission.objects.filter(team=self.team).filter(is_final=True).exists():
            self.valid = False
            self.errors.append("invitedTeamHasNoFinalSubmission")

    def _handle_lobby(self):
        if self.type == FriendlyGameTypes.SINGLE:
            self._single_lobby()
        elif self.multi_type == MultiFriendlyGameTypes.FRIEND:
            self._with_friend_multi_lobby()
        else:
            self._with_enemy_multi_lobby()

    def _single_lobby(self):
        with transaction.atomic():
            lobby = Lobby.objects.filter(completed=False).filter(multi_play=False).last()
            self.lobby = lobby if lobby else Lobby.objects.create()
            if not self._validate_lobby_join():
                return
            if self.lobby.teams1.count() < 2:
                self.lobby.teams1.add(self.request.user.participant.team)
            elif self.lobby.teams2.count() < 2:
                self.lobby.teams2.add(self.request.user.participant.team)
            if self.lobby.teams1.count() + self.lobby.teams2.count() >= 4:
                self.lobby.completed = True
                self.lobby.save()

    def _with_friend_multi_lobby(self):
        with transaction.atomic():
            lobby = Lobby.objects.filter(completed=False).filter(multi_play=True).filter(with_friend=True).last()
            self.lobby = lobby if lobby else Lobby.objects.create(multi_play=True, with_friend=True)
            if not self._validate_lobby_join():
                return
            if self.lobby.teams1.count() < 2:
                self.lobby.teams1.add(self.request.user.participant.team, self.team)
            elif self.lobby.teams2.count() < 2:
                self.lobby.teams2.add(self.request.user.participant.team, self.team)
            if self.lobby.teams1.count() + self.lobby.teams2.count() >= 4:
                self.lobby.completed = True
                self.lobby.save()

    def _with_enemy_multi_lobby(self):
        with transaction.atomic():
            lobby = Lobby.objects.filter(completed=False).filter(multi_play=True).filter(with_friend=False).last()
            self.lobby = lobby if lobby else Lobby.objects.create(multi_play=True, with_friend=False)
            if not self._validate_lobby_join():
                return
            if self.lobby.teams1.count() < 2 and self.lobby.teams2.count() < 2:
                self.lobby.teams1.add(self.request.user.participant.team)
                self.lobby.teams2.add(self.team)
            if self.lobby.teams1.count() + self.lobby.teams2.count() >= 4:
                self.lobby.completed = True
                self.lobby.save()

    def _validate_lobby_join(self):
        if self.lobby.teams1.filter(
                Q(name=self.request.user.participant.team.name) | Q(name=self.team_name)).exists() or \
                self.lobby.teams2.filter(
                    Q(name=self.request.user.participant.team.name) | Q(name=self.team_name)).exists():
            self.valid = False
            self.errors.append("alreadyJoined")
            return False
        return True
