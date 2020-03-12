from django.contrib import admin

from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from . import models as challenge_models


# Register your models here.

class GameTeamInline(NestedStackedInline):
    model = challenge_models.GameTeam


class GameSideInline(NestedStackedInline):
    model = challenge_models.GameSide
    inlines = [GameTeamInline]


class GameInline(admin.StackedInline):
    model = challenge_models.Game


@admin.register(challenge_models.Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'start_time', 'end_time']
    list_editable = ['name', 'type']


@admin.register(challenge_models.Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'start_time', 'submit_deadline']
    list_editable = ['type']


@admin.register(challenge_models.Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ['id', 'finished']
    list_editable = ['finished']


@admin.register(challenge_models.Group)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(challenge_models.GroupTeam)
class TeamGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(challenge_models.Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['id', '__str__', 'type', 'finished', 'time']
    list_filter = ['finished', 'type', 'time']

    inlines = [GameInline]


@admin.register(challenge_models.MatchTeam)
class MatchTeamAdmin(admin.ModelAdmin):
    pass


@admin.register(challenge_models.Game)
class GameAdmin(NestedModelAdmin):
    list_display = ['__str__', 'status', 'time', 'get_game_info', 'log']
    list_display_links = ['__str__']
    list_filter = ['status', 'time']
    search_fields = ['infra_token']
    inlines = [GameSideInline]

    def get_game_info(self, instance: challenge_models.Game):
        info = {}
        for i, game_side in enumerate(instance.game_sides.all()):
            info[f'Game_side {i + 1}'] = {'teams': '', 'score': 0}
            for game_team in game_side.game_teams.all():
                info[f'Game_side {i + 1}']['teams'] += game_team.team.name + " "
                info[f'Game_side {i + 1}']['score'] += game_team.score if game_team.score else 0
        return str(info)

    def get_tournament_name(self, instance: challenge_models.Game):
        return 'friendly' if not instance.match else instance.match.group.stage.tournament.name

    def get_teams_names(self, instance: challenge_models.Game):
        teams = []
        for game_side in instance.game_sides.all():
            for game_team in game_side.game_teams.all():
                teams.append(game_team.team.name)
        return ', '.join(teams)

    get_tournament_name.short_description = 'Tournament Name'
    get_teams_names.short_description = 'Teams Names'
    get_game_info.short_description = 'Game info'


@admin.register(challenge_models.GameSide)
class GameSideAdmin(admin.ModelAdmin):
    list_display = ['id', 'has_won']
    list_display_links = ['id']
    list_filter = ['has_won']
    inlines = [GameTeamInline]


@admin.register(challenge_models.GameTeam)
class GameTeamAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'game_side', 'score']
    list_display_links = ['__str__']
    sortable_by = ['score']


@admin.register(challenge_models.Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'language', 'submit_time', 'is_final', 'status']
    list_display_links = ['__str__']
    list_filter = ['language', 'submit_time', 'status', 'is_final']

    search_fields = ['infra_token', 'infra_compile_token']

    def get_team_name(self, instance: challenge_models.Submission):
        return instance.team.name

    get_team_name.short_description = 'Team name'

    def get_user_username(self, instance: challenge_models.Submission):
        return instance.user.username

    get_user_username.short_description = 'User username'


@admin.register(challenge_models.Map)
class MapAdmin(admin.ModelAdmin):
    pass


@admin.register(challenge_models.Lobby)
class LobbyAdmin(admin.ModelAdmin):
    list_display = ['id', 'match', 'completed', 'multi_play', 'with_friend']
    list_display_links = ['id']


@admin.register(challenge_models.RunTournament)
class RunTournamentAdmin(admin.ModelAdmin):
    list_display = ['id', 'tournament', 'finished']
    list_display_links = ['id', 'tournament']

    readonly_fields = ['finished']


@admin.register(challenge_models.RunGroup)
class RunGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'finished']
    list_display_links = ['id', 'group']

    readonly_fields = ['finished']


@admin.register(challenge_models.RunFinalMatch)
class RunFinalMatchAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_team', 'second_team']
    list_display_links = ['id']
