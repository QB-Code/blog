from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory, APIClient
from django.contrib.auth.models import User
from users.models import MyUser, Comment
from django.urls import reverse

from users.views import CommentsView
from posts.models import Post


factory = APIRequestFactory()


class CommentsTests(APITestCase):

    def setUp(self):
        user = User.objects.create_user(username='Dimon', password='1')
        my_user = MyUser.objects.create(user=user)

        self.post = Post.objects.create()

        self.client.login(username='Dimon', password='1')

    def test_add_comment(self):

        response = self.client.post(reverse('api/comments'), {'content': 'Test comment'})

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
