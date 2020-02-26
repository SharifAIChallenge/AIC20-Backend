from django.contrib import admin

from . import models as challenge_models


# Register your models here.


@admin.register(challenge_models.Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'start_time', 'end_time']
    list_editable = ['name', 'type']


@admin.register(challenge_models.Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'start_time', 'submit_deadline']
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
    list_filter = ['status']


@admin.register(challenge_models.GameSide)
class GameSideAdmin(admin.ModelAdmin):
    list_display = ['id', 'has_won']


@admin.register(challenge_models.GameTeam)
class GameTeamAdmin(admin.ModelAdmin):
    pass


@admin.register(challenge_models.Submission)
class SubmissionAdmin(admin.ModelAdmin):
    pass


@admin.register(challenge_models.Map)
class MapAdmin(admin.ModelAdmin):
    pass


@admin.register(challenge_models.Lobby)
class LobbyAdmin(admin.ModelAdmin):
    pass
