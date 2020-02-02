from django.contrib import admin

from . import models as faq_models


# Register your models here.

@admin.register(faq_models.QuestionWithAnswer)
class QuestionWithAnswer(admin.ModelAdmin):
    list_display = ['id', 'question_en', 'question_fa', 'answer_en', 'answer_fa']
    list_editable = ['question_en', 'question_fa', 'answer_en', 'answer_fa']
    list_display_links = ['id']
    sortable_by = ['id', 'question_en', 'question_fa', 'answer_en', 'answer_fa']
    search_fields = ['question_en', 'question_fa', 'answer_en', 'answer_fa']
