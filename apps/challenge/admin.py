from django.contrib import admin

from . import models as challenge_models


# Register your models here.


@admin.register(challenge_models.Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    pass


@admin.register(challenge_models.Tournament)
class TournamentAdmin(admin.ModelAdmin):
    pass


@admin.register(challenge_models.Stage)
class StageAdmin(admin.ModelAdmin):
    pass


@admin.register(challenge_models.Group)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(challenge_models.TeamGroup)
class TeamGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(challenge_models.Match)
class MathAdmin(admin.ModelAdmin):
    pass


@admin.register(challenge_models.MatchTeam)
class MatchTeamAdmin(admin.ModelAdmin):
    pass


@admin.register(challenge_models.Game)
class GameAdmin(admin.ModelAdmin):
    pass


@admin.register(challenge_models.GameSide)
class GameSideAdmin(admin.ModelAdmin):
    pass


@admin.register(challenge_models.GameTeam)
class GameTeamAdmin(admin.ModelAdmin):
    pass


@admin.register(challenge_models.Info)
class InfoAdmin(admin.ModelAdmin):
    pass


@admin.register(challenge_models.Submission)
class SubmissionAdmin(admin.ModelAdmin):
    pass


@admin.register(challenge_models.Map)
class MapAdmin(admin.ModelAdmin):
    pass
