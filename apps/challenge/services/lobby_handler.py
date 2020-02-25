import json

from django.db import transaction
from django.db.models import Q
from rest_framework.generics import get_object_or_404

from apps.challenge.models import Lobby
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
        self.team: Team = Team()
        self.lobby: Lobby = Lobby()
        self.errors = []
        self.friendly_game = None
        self.valid = True

    def __call__(self):
        self._set_type()
        if self.type == FriendlyGameTypes.MULTI:
            self._set_multi_type()
            self._set_team_name()
        if self.valid:
            self._handle_lobby()
        if self.lobby.completed:
            self.friendly_game = FriendlyGameCreator(lobby=self.lobby)

        return self.errors, self.friendly_game

    def _set_type(self):
        self.type = self.data.get('type', FriendlyGameTypes.SINGLE)

    def _set_multi_type(self):
        self.multi_type = self.data.get('multi_type', MultiFriendlyGameTypes.FRIEND)

    def _set_team_name(self):
        self.team_name = self.data.get('team_name')
        if self.multi_type == FriendlyGameTypes.MULTI and not self.team_name:
            self.valid = False
            self.errors.append("Please give a team name")
            return
        if self.team_name == self.request.user.participant.team.name:
            self.valid = False
            self.errors.append("You cant't play with yourself")
            return
        self.team = get_object_or_404(Team, name=self.team_name)
        if self.team.allow_multi_friendly is False:
            self.valid = False
            self.errors.append("Entered team multi game is closed")

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
                self.lobby.teams1.add(self.request.user.participant.team)
            else:
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
            else:
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
            else:
                self.lobby.completed = True
                self.lobby.save()

    def _validate_lobby_join(self):
        if self.lobby.teams1.filter(
                Q(name=self.request.user.participant.team.name) | Q(name=self.team_name)).exists() or \
                self.lobby.teams2.filter(
                    Q(name=self.request.user.participant.team.name) | Q(name=self.team_name)).exists():
            self.valid = False
            self.errors.append("You or the team that you entered already joined this lobby")
            return True
        return False
