from django.db import models

# Create your models here.

class Blog(models.Model):
    image = models.ImageField()


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='posts')
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField()
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=10000)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    writer_name = models.CharField(max_length=50)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    shown = models.BooleanField(default=True)

class Tag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=50)
    # color = models


