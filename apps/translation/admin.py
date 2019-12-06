from django.contrib import admin
from .models import TranslatedText

@admin.register(TranslatedText)
class TranslatedTextAdmin(admin.ModelAdmin):
  pass
