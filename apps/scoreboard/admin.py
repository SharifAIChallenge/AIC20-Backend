from django.contrib import admin

from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from . import models as scoreboard_models


# Register your models here.

class RowInline(admin.StackedInline):
    model = scoreboard_models.Row


@admin.register(scoreboard_models.ScoreBoard)
class ScoreBoardAdmin(PolymorphicParentModelAdmin):
    inlines = [RowInline]
    base_model = scoreboard_models.ScoreBoard

    child_models = [scoreboard_models.ChallengeScoreBoard, scoreboard_models.GroupScoreBoard,
                    scoreboard_models.FriendlyScoreBoard
                    ]

    def has_add_permission(self, request):
        return False


@admin.register(scoreboard_models.ChallengeScoreBoard)
class ChallengeScoreBoardAdmin(PolymorphicChildModelAdmin):
    inlines = [RowInline]
    base_model = scoreboard_models.ScoreBoard
    show_in_index = True


@admin.register(scoreboard_models.GroupScoreBoard)
class GroupScoreBoardAdmin(PolymorphicChildModelAdmin):
    inlines = [RowInline]
    base_model = scoreboard_models.ScoreBoard
    show_in_index = True


@admin.register(scoreboard_models.FriendlyScoreBoard)
class FriendlyScoreBoardAdmin(PolymorphicChildModelAdmin):
    inlines = [RowInline]
    base_model = scoreboard_models.ScoreBoard
    show_in_index = True


@admin.register(scoreboard_models.Row)
class RowAdmin(admin.ModelAdmin):
    list_display = ['id', 'team', 'scoreboard', 'score', 'wins', 'loss', 'draws']
    list_display_links = ['id', 'team']
