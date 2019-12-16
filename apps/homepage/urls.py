from django.urls import path

from apps.homepage.views import *

app_name = 'homepage'
urlpatterns = [
    path('', get_homepage, name='get_homepage')
]
