from django.conf.urls import url
from django.urls import path, include
from blog.views import *

urlpatterns = [

    url(r'^$', BlogView.as_view()),
    path('<int:post_id>', PostView.as_view()),
    path('<int:post_id>/comments', CommentListView.as_view()),

]
