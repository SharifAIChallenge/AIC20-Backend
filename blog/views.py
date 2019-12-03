from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from blog.models import *
from blog.serializers import *
from blog import paginations


# Create your views here.

class blog_view(GenericAPIView):

    serializer_class = BlogSerializer
    queryset =  [Blog.objects.all()],
    def get(self,request):
        data = BlogSerializer(self.get_queryset()).data
        return Response(data)

class post_list_view(GenericAPIView):

    serializer_class = PostSerializer
    queryset =  [Post.objects.all()],
    def get(self,request):
        data = PostSerializer(self.get_queryset(), many=True).data
        return Response(data)


class comment_list_view(GenericAPIView):
    serializer_class = CommentSerializer
    queryset = [Comment.objects.all()]

    #TODO IsAuthenticated
    # permission_classes = ['IsAuthenticated|IsReadOnlyRequest']
    pagination_class = paginations.CommentsPagination

    def get(self, request):
        data = CommentSerializer(self.get_queryset(), many=True).data
        return Response(data)

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": ("کامنت شما ثبت شد.")})



