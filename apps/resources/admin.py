from martor.widgets import AdminMartorWidget

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db import models

from .models import Document, Section, Subsection


# Register your models here.

class SectionInline(admin.StackedInline):
    model = Section
    readonly_fields = ['uuid']
#    formfield_overrides = {
#        models.TextField: {'widget': AdminMartorWidget},
#    }


class SubtitleInline(admin.StackedInline):
    model = Subsection


@admin.register(Document)
class DocumentAdmin(ModelAdmin):
    list_display = ['id', 'title_en', 'title_fa']
    list_display_links = ['id']
    list_editable = ['title_en', 'title_fa']
    search_fields = ['title_en', 'title_fa']
    sortable_by = ['title_en', 'title_fa']
    inlines = [SectionInline]
    pass


@admin.register(Section)
class SectionAdmin(ModelAdmin):
    list_display = ['id', 'uuid', 'title_en', 'title_fa', 'get_document_title']
    list_display_links = ['id', 'uuid']
    list_editable = ['title_en', 'title_fa']
    readonly_fields = ['uuid']
    search_fields = ['title_en', 'title_fa']
    sortable_by = ['title_en', 'title_fa']
    inlines = [SubtitleInline]
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

    def get_document_title(self, section: Section):
        return section.document.title_en

    get_document_title.short_description = 'Document Title'
    get_document_title.admin_order_field = 'section_document_title'

    pass


@admin.register(Subsection)
class SubtitleAdmin(ModelAdmin):
    list_display = ['id', 'subtitle_en', 'subtitle_fa']
    list_display_links = ['id']
    list_editable = ['subtitle_en', 'subtitle_fa']
    search_fields = ['subtitle_en', 'subtitle_fa']

    pass
