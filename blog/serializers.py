from rest_framework import serializers
from blog.models import *


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['image','posts' ]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['date', 'image', 'title', 'text', 'comments', 'tags']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['writer_name', 'text', 'date', 'email', 'shown']
    def validate(self , attrs):
        if not attrs['shown']:
            raise serializers.ValidationError("این کامنت قابل نمایش نیست!")
        return attrs


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'color']
