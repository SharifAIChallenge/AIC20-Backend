from apps.accounts.models import Profile
from django.contrib import admin

# Register your models here


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = [
        'firstname_fa',
        'firstname_en',
        'lastname_fa',
        'lastname_en',
        'birth_date',
        'university',
    ]

