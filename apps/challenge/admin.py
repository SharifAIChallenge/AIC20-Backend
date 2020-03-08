from django.contrib import admin

from . import models as challenge_models


# Register your models here.

class GameTeamInline(admin.StackedInline):
    model = challenge_models.GameTeam


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
class MathAdmin(admin.ModelAdmin):
    list_display = ['id', 'type']
    list_editable = ['type']


@admin.register(challenge_models.MatchTeam)
class MatchTeamAdmin(admin.ModelAdmin):
    pass


@admin.register(challenge_models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'status', 'time', 'get_tournament_name']
    list_display_links = ['__str__']
    list_filter = ['status', 'time']

    def get_tournament_name(self, instance: challenge_models.Game):
        return 'friendly' if not instance.match else instance.match.group.stage.tournament.name

    get_tournament_name.short_description = 'Tournament Name'


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
    list_display_links = ['id', 'tournament']

    readonly_fields = ['finished']
