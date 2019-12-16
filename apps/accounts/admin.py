from apps.accounts.models import Profile
from django.contrib import admin

# Register your models here


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'first_name_en', 'last_name_en', 'birth_date', 'residence', 'education']
