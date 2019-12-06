from apps.accounts.models import Profile
from django.contrib import admin

# Register your models here
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'password']
