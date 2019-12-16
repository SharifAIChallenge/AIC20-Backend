from django.db import models


class Post(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField()
    title_en = models.CharField(max_length=50)
    title_fa = models.CharField(max_length=50)
    text_en = models.TextField(max_length=10000)
    text_fa = models.TextField(max_length=10000)
    description_fa = models.TextField(max_length=300)
    description_en = models.TextField(max_length=300)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    writer_name = models.CharField(max_length=50)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    shown = models.BooleanField(default=True)
    reply_to = models.ForeignKey(
        'Comment', on_delete=models.CASCADE, null=True, blank=True)


class Tag(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='tags')
    name_en = models.CharField(max_length=50)
    name_fa = models.CharField(max_length=50)
    color = models.CharField(max_length=20)
