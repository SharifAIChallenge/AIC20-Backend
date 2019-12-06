from django.contrib import admin
from .models import TranslatedText, DocumentTest


@admin.register(TranslatedText)
class TranslatedTextAdmin(admin.ModelAdmin):
    pass


@admin.register(DocumentTest)
class DocumentTestAdmin(admin.ModelAdmin):
    pass
