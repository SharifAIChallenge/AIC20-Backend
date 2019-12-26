from django.contrib import admin
from django.contrib.admin import ModelAdmin
from apps.uploads.models import FileUpload


@admin.register(FileUpload)
class FileUploadAdmin(ModelAdmin):
    list_display = ['name', '__str__']
    list_editable = []
    pass
