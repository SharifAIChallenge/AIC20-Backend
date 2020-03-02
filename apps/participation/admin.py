from django.contrib import admin

from .models import Badge, Participant, Team, Invitation


class ParticipantInline(admin.StackedInline):
    model = Participant


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    pass


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_display_links = ['__str__']
    search_fields = ['get_username', 'get_team_name']

    def get_username(self, instance: Participant):
        return instance.user.username

    get_username.short_description = 'Username'

    def get_team_name(self, instance: Participant):
        return instance.team.name

    get_team_name.short_description = 'Team name'


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'challenge', 'allow_multi_friendly']
    list_display_links = ['id', 'name']
    list_editable = ['allow_multi_friendly']

    inlines = [ParticipantInline]


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'status']
    list_display_links = ['__str__']
