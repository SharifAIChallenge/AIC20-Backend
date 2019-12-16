from martor.widgets import AdminMartorWidget

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db import models

from django_reverse_admin import ReverseModelAdmin, ReverseInlineModelAdmin

from apps.translation.admin import TranslatedTextInlineSmall, TranslatedTextInlineLarge
from .models import Document, Section, Subsection


# Register your models here.

class SectionInline(ReverseInlineModelAdmin):
    model = Section
    readonly_fields = ['uuid']
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


class SubtitleInline(ReverseInlineModelAdmin):
    model = Subsection


@admin.register(Document)
class DocumentAdmin(ReverseModelAdmin):
    list_display = ['id', '__str__']
    list_display_links = ['id', '__str__']
    search_fields = ['__str__']
    sortable_by = ['__str__', 'id']
    inline_type = 'stacked'
    inline_reverse = [
        {
            'field_name': 'sections',
            'kwargs': {},
            'admin_class': SectionInline
        },
        {
            'field_name': 'title',
            'kwargs': {},
            'admin_class': TranslatedTextInlineSmall
        },
        {
            'field_name': 'description',
            'kwargs': {},
            'admin_class': TranslatedTextInlineLarge
        },
    ]
    pass


@admin.register(Section)
class SectionAdmin(ReverseModelAdmin):
    list_display = ['id', 'uuid', '__str__', 'get_document_title']
    list_display_links = ['id', 'uuid', '__str__']
    readonly_fields = ['uuid']
    search_fields = ['__str__', 'uuid', 'get_document_title']
    sortable_by = ['__str__']
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

    def get_document_title(self, section: Section):
        return section.document.title.content_en

    get_document_title.short_description = 'Document Title'
    get_document_title.admin_order_field = 'section_document_title'

    inline_type = 'stacked'
    inline_reverse = [
        {
            'field_name': 'subtitles',
            'kwargs': {},
            'admin_class': SubtitleInline
        },
        {
            'field_name': 'title',
            'kwargs': {},
            'admin_class': TranslatedTextInlineSmall
        },
    ]
    pass


@admin.register(Subsection)
class SubtitleAdmin(ReverseModelAdmin):
    list_display = ['id', '__str__']
    list_display_links = ['id', '__str__']
    search_fields = ['__str__', 'get_section_title']
    inline_type = 'stacked'
    inline_reverse = [
        {
            'field_name': 'subtitle',
            'kwargs': {},
            'admin_class': TranslatedTextInlineSmall
        },
    ]

    def get_section_title(self, section: Section):
        return section.document.title.content_en

    get_section_title.short_description = 'Section Title'
    get_section_title.admin_order_field = 'subsection_section_title'

    pass
