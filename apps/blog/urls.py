from django.conf.urls import url
from django.urls import path

from apps.blog.views import BlogView, PostView, CommentListView

urlpatterns = [

    path('', BlogView.as_view()),
    path('<int:post_id>', PostView.as_view()),
    path('<int:post_id>/comments', CommentListView.as_view()),

]
