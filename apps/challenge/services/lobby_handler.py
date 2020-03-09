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

    def __init__(self, lobby, final=False):
        self.lobby = lobby
        self.final = final
        self.friendly_game = ''
        self.friendly_game_teams = []
        self.friendly_game_sides = []

    def __call__(self, *args, **kwargs):
        self._create_friendly_game()
        self._create_game_sides()
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
            if self.final:
                self.friendly_game_teams.append(
                    GameTeam.objects.create(team=team, game_side=self.friendly_game_sides[0]))
        for team in self.lobby.teams2.all():
            self.friendly_game_teams.append(
                GameTeam.objects.create(team=team, game_side=self.friendly_game_sides[1])
            )
            if self.final:
                self.friendly_game_teams.append(
                    GameTeam.objects.create(team=team, game_side=self.friendly_game_sides[1])
                )


class LobbyHandler:

    def __init__(self, request):
        self.request = request
        self.team = request.user.participant.team
        self.data = json.loads(request.body)
        self.type = ''
        self.multi_type = ''
        self.team_name = ''
        self.invited_team = None
        self.lobby = None
        self.errors = []
        self.friendly_game = None
        self.valid = True

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
            self.friendly_game = FriendlyGameCreator(lobby=self.lobby,
                                                     final=self.team.challenge.type == ChallengeTypes.FINAL)()

        return self.errors, self.friendly_game

    def _validate_friendly_delay(self):
        challenge = self.team.challenge
        last_friendly_game_time = GameTeam.objects.filter(team=self.team).filter(
            game_side__game__match=None).order_by('game_side__game__time').values_list('game_side__game__time',
                                                                                       flat=True).last()
        if last_friendly_game_time and datetime.now(utc) - last_friendly_game_time < timedelta(
                minutes=challenge.friendly_game_delay):
            self.valid = False
            self.errors.append(f"pleaseWait")

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
        if self.team_name == self.team.name:
            self.valid = False
            self.errors.append("cantInviteYourself")
            return
        self.invited_team = get_object_or_404(Team, name=self.team_name)
        if not self.invited_team.allow_multi_friendly:
            self.valid = False
            self.errors.append("doesntAcceptInvitation")
        if not self.team.allow_multi_friendly:
            self.valid = False
            self.errors.append("pleaseEnableInvitation")

    def _validate_teams(self):
        if not self.team.is_valid:
            self.valid = False
            self.errors.append("teamInvalid")
            return
        if not Submission.objects.filter(team=self.team).filter(is_final=True).exists():
            self.valid = False
            self.errors.append("teamHasNoFinalSubmission")
        if self.invited_team and not self.invited_team.is_valid:
            self.valid = False
            self.errors.append("invitedTeamInvalid")
            return
        if self.invited_team and not Submission.objects.filter(team=self.invited_team).filter(is_final=True).exists():
            self.valid = False
            self.errors.append("invitedTeamHasNoFinalSubmission")

        if self.invited_team and self.invited_team.challenge != self.team.challenge:
            self.valid = False
            self.errors.append("notSameChallenge")

    def _handle_lobby(self):

        if self.type == FriendlyGameTypes.SINGLE:
            if self.team.challenge.type == ChallengeTypes.FINAL:
                self._single_lobby_final()
            else:
                self._single_lobby()
        elif self.multi_type == MultiFriendlyGameTypes.FRIEND:
            self._with_friend_multi_lobby()
        else:
            if self.team.challenge.type == ChallengeTypes.FINAL:
                self._with_enemy_multi_lobby_final()
            else:
                self._with_enemy_multi_lobby()

    def _single_lobby_final(self):
        with transaction.atomic():
            lobby = Lobby.objects.filter(completed=False).filter(multi_play=False).filter(
                challenge=self.team.challenge).last()
            self.lobby = lobby if lobby else Lobby.objects.create(challenge=self.team.challenge)
            if not self._validate_lobby_join():
                return
            if self.lobby.teams1.count() < 1:
                self.lobby.teams1.add(self.team, self.team)
            elif self.lobby.teams2.count() < 1:
                self.lobby.teams2.add(self.team, self.team)
            if self.lobby.teams1.count() + self.lobby.teams2.count() >= 2:
                self.lobby.completed = True
                self.lobby.save()

    def _single_lobby(self):
        with transaction.atomic():
            lobby = Lobby.objects.filter(completed=False).filter(multi_play=False).last()
            self.lobby = lobby if lobby else Lobby.objects.create(challenge=self.team.challenge)
            if not self._validate_lobby_join():
                return
            if self.lobby.teams1.count() < 2:
                self.lobby.teams1.add(self.team)
            elif self.lobby.teams2.count() < 2:
                self.lobby.teams2.add(self.team)
            if self.lobby.teams1.count() + self.lobby.teams2.count() >= 4:
                self.lobby.completed = True
                self.lobby.save()

    def _with_friend_multi_lobby(self):
        with transaction.atomic():
            lobby = Lobby.objects.filter(completed=False).filter(challenge=self.team.challenge).filter(
                multi_play=True).filter(with_friend=True).last()
            self.lobby = lobby if lobby else Lobby.objects.create(multi_play=True, with_friend=True,
                                                                  challenge=self.team.challenge)
            if not self._validate_lobby_join():
                return
            if self.lobby.teams1.count() < 2:
                self.lobby.teams1.add(self.team, self.invited_team)
            elif self.lobby.teams2.count() < 2:
                self.lobby.teams2.add(self.team, self.invited_team)
            if self.lobby.teams1.count() + self.lobby.teams2.count() >= 4:
                self.lobby.completed = True
                self.lobby.save()

    def _with_enemy_multi_lobby(self):
        with transaction.atomic():
            lobby = Lobby.objects.filter(completed=False).filter(challenge=self.team.challenge).filter(
                multi_play=True).filter(with_friend=False).last()
            self.lobby = lobby if lobby else Lobby.objects.create(multi_play=True, with_friend=False,
                                                                  challenge=self.team.challenge)
            if not self._validate_lobby_join():
                return
            if self.lobby.teams1.count() < 2 and self.lobby.teams2.count() < 2:
                self.lobby.teams1.add(self.team)
                self.lobby.teams2.add(self.invited_team)
            if self.lobby.teams1.count() + self.lobby.teams2.count() >= 4:
                self.lobby.completed = True
                self.lobby.save()

    def _with_enemy_multi_lobby_final(self):
        with transaction.atomic():
            lobby = Lobby.objects.filter(completed=False).filter(challenge=self.team.challenge).filter(
                multi_play=True).filter(with_friend=False).last()
            self.lobby = lobby if lobby else Lobby.objects.create(multi_play=True, with_friend=False,
                                                                  challenge=self.team.challenge)
            if not self._validate_lobby_join():
                return
            if self.lobby.teams1.count() < 1 and self.lobby.teams2.count() < 1:
                self.lobby.teams1.add(self.team)
                self.lobby.teams2.add(self.invited_team)
            if self.lobby.teams1.count() + self.lobby.teams2.count() >= 2:
                self.lobby.completed = True
                self.lobby.save()

    def _validate_lobby_join(self):
        if self.lobby.teams1.filter(
                Q(name=self.team.name) | Q(name=self.team_name)).exists() or \
                self.lobby.teams2.filter(Q(name=self.team.name) | Q(name=self.team_name)).exists():
            self.valid = False
            self.errors.append("alreadyJoined")
            return False
        return True
