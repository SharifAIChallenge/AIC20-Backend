from django.contrib import admin

from . import models as faq_models


# Register your models here.

class AnswerInline(admin.StackedInline):
    model = faq_models.Answer


@admin.register(faq_models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'question']
    list_display_links = ['id', 'question']
    list_editable = ['title']
    sortable_by = ['id', 'title', 'question']
    search_fields = ['title']


@admin.register(faq_models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'get_answer_id']
    list_editable = ['title']
    list_display_links = ['id', 'get_answer_id']
    sortable_by = ['id', 'title', 'get_answer_id']
    search_fields = ['title']
    inlines = [AnswerInline]

    def get_answer_id(self, question: faq_models.Question):
        return question.answer.id

    get_answer_id.short_description = 'Answer ID'
    get_answer_id.admin_order_field = 'question_answer_id'
