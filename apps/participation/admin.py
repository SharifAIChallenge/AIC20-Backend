from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Badge, Participant, Team

@admin.register(Badge)
class BadgeAdmin(ModelAdmin):
    pass

@admin.register(Participant)
class ParticipantAdmin(ModelAdmin):
    pass

@admin.register(Team)
class TeamAdmin(ModelAdmin):
    pass