from django.urls import path

from homepage import views

app_name = 'homepage'
urlpatterns = [
    path('', views.get_homepage, name='get_homepage')
]