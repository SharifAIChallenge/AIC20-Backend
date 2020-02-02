from django.contrib import admin

from . import models as staff_models


# Register your models here.

@admin.register(staff_models.Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['id', 'group_title', 'team_title', 'first_name_en', 'last_name_en']
    list_editable = ['group_title', 'team_title']
    list_display_links = ['id', 'first_name_en', 'last_name_en']
    search_fields = ['group_title', 'team_title', 'first_name_en', 'last_name_en']
    sortable_by = ['id', 'group_title', 'team_title', 'first_name_en', 'last_name_en']
    list_filter = ['group_title', 'team_title']
