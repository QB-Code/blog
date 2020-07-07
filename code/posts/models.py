from django.db import models
from users.models import MyUser


class Rubric(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=200)
    picture = models.ImageField(upload_to='posts/rubric_image')
    subscriber_count = models.IntegerField(default=0)


class Post(models.Model):
    header = models.CharField(max_length=30)
    content = models.TextField()
    picture = models.ImageField(upload_to='posts/post_image', null=True)
    rating = models.IntegerField(default=0)
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='user_posts')
    rated_users = models.ManyToManyField(MyUser, related_name='ratings', blank=True)


class PostPhoto(models.Model):
    image = models.ImageField(upload_to='posts/post_photo')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
