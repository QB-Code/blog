from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):
    picture = models.ImageField(null=True, upload_to='users/avatars')
    description = models.TextField(null=True)
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.TextField()
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='comments')
    rated_users = models.ManyToManyField(MyUser, related_name='rated_comments')


class CommentPhoto(models.Model):
    picture = models.ImageField(upload_to='users/comments/comments_photo')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

