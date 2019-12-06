from django.db.models import F

def translateQuerySet(querySet, language, fields):
  lang = language[:2]
  if lang != 'en' and lang != 'fa':
    lang = 'fa'
  return querySet.annotate(**{ 
    field+"_value" : F(field+"__content_"+lang) for field in fields 
  })