from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class MyUser(models.Model):
    picture = models.ImageField(null=True, upload_to='users/avatars')
    description = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='my_user')
    bookmarks = models.ManyToManyField('posts.Post', blank=True, through='users.Bookmark')
    subscribed_rubrics = models.ManyToManyField('posts.Rubric', blank=True)
    subscribed_users = models.ManyToManyField('self', blank=True)


class Bookmark(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    my_user = models.ForeignKey(MyUser, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.TextField(default='')
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    released_at = models.DateTimeField(null=True)
    is_released = models.BooleanField(default=False)

    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='comments')
    rated_users = models.ManyToManyField(MyUser, blank=True, related_name='rated_comments', through='users.CommentRate')

    class Meta:
        ordering = ('released_at', )

    def to_dict(self):
        return {
            'pk': self.pk,
            'content': self.content,
        }


class CommentPhoto(models.Model):
    picture = models.ImageField(upload_to='users/comments/photos')
    comment = models.ForeignKey(Comment, blank=True, related_name='photos', on_delete=models.CASCADE)


class CommentRate(models.Model):
    like = models.BooleanField()
    author = models.ForeignKey(MyUser, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, blank=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('author', 'comment')


