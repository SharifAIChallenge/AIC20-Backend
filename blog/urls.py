from django.conf.urls import url
from django.urls import path, include
from blog.views import *

urlpatterns = [

    url(r'^$', blog_view.as_view()),
    path('post/<int:id>', post_list_view.as_view()),
    url(r'^comment/$', comment_list_view.as_view()),

]
