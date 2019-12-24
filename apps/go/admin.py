from django.contrib import admin
from django.contrib.admin import ModelAdmin
from apps.go.models import Redirect

# Register your models here.

@admin.register(Redirect)
class RedirectAdmin(ModelAdmin):
    pass
