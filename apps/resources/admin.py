from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Document, Section, Subtitle


# Register your models here.

@admin.register(Document)
class DocumentAdmin(ModelAdmin):
    list_display = ['title']
    pass


@admin.register(Section)
class SectionAdmin(ModelAdmin):
    list_display = ['title', 'md', 'get_document_title']

    def get_document_title(self, section: Section):
        return section.document.title

    get_document_title.short_description = 'Author'
    get_document_title.admin_order_field = 'book__author'

    pass


@admin.register(Subtitle)
class SubtitleAdmin(ModelAdmin):
    list_display = ['subtitle']

    pass
