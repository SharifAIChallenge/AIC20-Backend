from django.http import Http404
from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS, BasePermission, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from blog.models import *
from blog.serializers import *
from blog import paginations


# Create your views here.

class BlogView(GenericAPIView):
    serializer_class = PostDescriptionSerializer
    queryset = Post.objects.all()

    def get(self, request):
        data = PostDescriptionSerializer(self.get_queryset(), many=True).data
        return Response(data)


class PostView(GenericAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get(self, request, post_id):
        try:
            data = PostSerializer(self.get_queryset().get(pk=post_id)).data
            return Response(data)
        except Post.DoesNotExist:
            raise Http404


class CommentListView(GenericAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = paginations.CommentsPagination

    def get_queryset(self):
        return Comment.objects.all().exclude(shown=False)

    def get(self, request, post_id):
        try:
            comments = self.get_queryset().filter(post__id=post_id)
            data = CommentSerializer(comments).data
            return Response(data)
        except comments.DoesNotExist:
            raise Http404

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "کامنت شما ثبت شد."})
