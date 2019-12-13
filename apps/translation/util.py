from django.db.models import F
from .models import TranslatedText

def translateQuerySet(querySet, request):
    language = request.headers['Accept-language']
    lang = language[:2]
    if lang != 'en' and lang != 'fa':
        lang = 'fa'
    fields = [ field.name for field in querySet.model._meta.fields
    if field.related_model == TranslatedText ]
    return querySet.annotate(**{
        field+"_value": F(field+"__content_"+lang) for field in fields
    })
