from django.conf.urls import url
from django.urls import path, include
from blog.views import *

urlpatterns = [

    url(r'^$', blog_view.as_view()),
    path('posts/', post_list_view.as_view()),
    path('posts/<int:id>', post_by_id_view.as_view()),
    url(r'^comments/$', comment_list_view.as_view()),

]
