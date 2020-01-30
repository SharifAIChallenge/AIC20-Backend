from django.contrib import admin

from . import models as staff_models


# Register your models here.

@admin.register(staff_models.Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'first_name', 'last_name']
    list_editable = ['title']
    list_display_links = ['id', 'first_name', 'last_name']
    search_fields = ['title', 'first_name', 'last_name']
    sortable_by = ['id', 'title', 'first_name', 'last_name']
    list_filter = ['title']
