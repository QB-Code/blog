import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from posts.models import Post
from users.models import MyUser, Comment


class CommentsViewsTestsBase(APITestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='User1', password='1')
        self.user1 = MyUser.objects.create(user=user1)

        user2 = User.objects.create_user(username='User2', password='1')
        self.user2 = MyUser.objects.create(user=user2)

        self.post = Post.objects.create(content='Post content', header='Post header', author=self.user1)
        self.old_comment_content = 'Comment by user1 content'
        self.new_comment_content = 'Comment by user1, but edited'
        self.comment_by_user1 = Comment.objects.create(author=self.user1, post=self.post,
                                                       content=self.old_comment_content)

        self.client.login(username='User1', password='1')


class CommentsViewTests(CommentsViewsTestsBase):
    comment_content = 'Some comment content'

    def test_post__authorized_user__comment_creates_successfully_201(self):
        response = self.client.post(reverse('api/comments'),
                                    {'content': self.comment_content, 'post': self.post.pk})

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        expected_comment_id = json.loads(response.content)['value']['pk']

        try:
            actual_comment = Comment.objects.get(pk=expected_comment_id)
        except Comment.DoesNotExist:
            self.fail("Comment with such id don't exist")

        self.assertTrue(actual_comment.content == self.comment_content, actual_comment.author == self.user1)

    def test_post__unauthorized_user__failed_401(self):
        self.client.logout()
        response = self.client.post(reverse('api/comments'),
                                    {'content': self.comment_content, 'post': self.post.pk})

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class CommentViewTests(CommentsViewsTestsBase):
    def test_delete__wrong_comment_url__failed_404(self):
        response = self.client.delete(reverse('api/comment', kwargs={'comment_id': 12321}))

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_delete__unauthenticated_user__failed_401(self):
        self.client.logout()
        response = self.client.delete(reverse('api/comment', kwargs={'comment_id': self.comment_by_user1.pk}))

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        if not Comment.objects.filter(pk=self.comment_by_user1.pk).exists():
            self.fail('Comment deleted by unauthenticated user')

    def test_delete__unauthorized_user__failed_401(self):
        self.client.login(username='User2', password='1')
        response = self.client.delete(reverse('api/comment', kwargs={'comment_id': self.comment_by_user1.pk}))

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        if not Comment.objects.filter(pk=self.comment_by_user1.pk).exists():
            self.fail('Comment deleted by unauthorized user')

    def test_delete__authorized_user__deleted_200(self):
        response = self.client.delete(reverse('api/comment', kwargs={'comment_id': self.comment_by_user1.pk}))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        if Comment.objects.filter(pk=self.comment_by_user1.pk).exists():
            self.fail('Comment want deleted')

    def test_patch__wrong_comment_url__failed_404(self):
        response = self.client.patch(reverse('api/comment', kwargs={'comment_id': 12321}))

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_patch__unauthenticated_user__failed_401(self):
        self.client.logout()
        response = self.client.patch(reverse('api/comment', kwargs={'comment_id': self.comment_by_user1.pk}),
                                     {'content': self.new_comment_content})

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        actual_comment_content = Comment.objects.get(pk=self.comment_by_user1.pk).content
        self.assertEqual(self.old_comment_content, actual_comment_content)

    def test_patch__unauthorized_user__failed_401(self):
        self.client.login(username='User2', password='1')
        response = self.client.patch(reverse('api/comment', kwargs={'comment_id': self.comment_by_user1.pk}),
                                     {'content': self.new_comment_content})

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        actual_comment_content = Comment.objects.get(pk=self.comment_by_user1.pk).content
        self.assertEqual(self.old_comment_content, actual_comment_content)

    def test_patch__authorized_user__patched_200(self):
        response = self.client.patch(reverse('api/comment', kwargs={'comment_id': self.comment_by_user1.pk}),
                                     {'content': self.new_comment_content})

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        actual_comment_content = Comment.objects.get(pk=self.comment_by_user1.pk).content
        self.assertEqual(self.new_comment_content, actual_comment_content)



