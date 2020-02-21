from django.db import models
from django.contrib.auth.models import User


class MyUser(User):
    picture = models.ImageField(null=True)
    description = models.TextField(null=True)
    rating = models.IntegerField(default=0)


class Comment(models.Model):
    content = models.TextField()
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='comments')
    rated_users = models.ManyToManyField(MyUser, related_name='rated_comments')


class CommentPhoto(models.Model):
    picture = models.ImageField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

