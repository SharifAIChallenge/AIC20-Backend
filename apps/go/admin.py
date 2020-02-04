import csv

from django.http import HttpResponse
from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.go.models import Redirect


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


@admin.register(Redirect)
class RedirectAdmin(ModelAdmin, ExportCsvMixin):
    list_display = ['source', 'destination', 'hits']
    sortable_by = ['source', 'destination', 'hits']
    readonly_fields = ['hits']

    actions = ['export_as_csv']


