from django.db import models
from django.contrib.auth.models import User
import datetime


class MyUser(models.Model):
    picture = models.ImageField(null=True, upload_to='users/avatars')
    description = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='my_user')
    bookmarks = models.ManyToManyField('posts.Post', blank=True)
    subscribed_rubrics = models.ManyToManyField('posts.Rubric', blank=True)
    subscribed_users = models.ManyToManyField('self', blank=True)


class Comment(models.Model):
    content = models.TextField()
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='comments')
    rated_users = models.ManyToManyField(MyUser, blank=True, related_name='rated_comments', through='users.CommentRate')

    class Meta:
        ordering = ('created_at', )


class CommentPhoto(models.Model):
    picture = models.ImageField(upload_to='users/comments/comments_photo')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


class CommentRate(models.Model):
    like = models.BooleanField()
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


