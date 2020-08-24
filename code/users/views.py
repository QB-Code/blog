from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated

from .models import MyUser, Bookmark, CommentPicture, Comment, CommentRate
from .serializers import (
    UserSerializer,
    LoginSerializer,
    CommentSerializer,
    InitCommentPictureSerializer,
    CommentPictureSerializer,
    CommentRateSerializer,
    BookmarkSerializer,
)
from .tokens import email_confirm_token_generator
from .utils import send_email_confirmation, set_default_user_pic


def email_confirm(request, user_id, token):
    try:
        user = User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        return HttpResponse('There isn`t user with such id')

    if email_confirm_token_generator.check_token(user=user, token=token):
        user.is_active = True
        user.save()
        login(request, user=user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/')
    else:
        return HttpResponse('Token doesnt mush')


# Convenient way to see current user, for development purposes only
def user_test_page(request):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f'username: {user.username}, is_active: {user.is_active}')
    else:
        return HttpResponse('User isn`t log in')


def user_page(request, user_id):
    return render(request, template_name='users/user.html')


def password_reset(request):
    return render(request, template_name='users/password-reset-confirm.html')


class SingUpView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()
            my_user = MyUser(user=new_user)
            send_email_confirmation(user=new_user)
            set_default_user_pic(my_user=my_user, username=new_user.username)

            return Response({'status': 'created',
                             'message': 'Confirm email',
                             'value': serializer.data},
                            status=status.HTTP_201_CREATED)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = authenticate(request=request, **serializer.data)
            if user is not None:
                login(request=request, user=user)
                return Response({'status': 'ok', 'message': 'User successfully logged in'})
            else:
                return Response({'status': 'error', 'message': 'Username or password is incorrect'},
                                status=status.HTTP_400_BAD_REQUEST)


class CommentsView(APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            comment = serializer.save()
            comment.author = request.user.my_user
            comment.is_released = True
            comment.released_at = timezone.now()
            comment.save()

            return Response({'status': 'created',
                             'value': comment.to_dict()},
                            status=status.HTTP_201_CREATED)


class CommentView(APIView):
    serializer_class = CommentSerializer

    def patch(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)

        if not comment.author.user == request.user:
            return Response({'status': 'error'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CommentSerializer(instance=comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            comment = serializer.save()
            return Response({'status': 'patched', 'value': comment.to_dict()})

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)

        if not comment.author.user == request.user:
            return Response({'status': 'error'}, status=status.HTTP_401_UNAUTHORIZED)

        for picture in comment.pictures.all():
            picture.picture.delete(save=False)

        comment.delete()

        return Response({'status': 'deleted', 'message': 'Comment successfully deleted'})


class CommentsPhotosView(APIView):
    serializer_class = InitCommentPictureSerializer
    parser_class = (FileUploadParser,)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = InitCommentPictureSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            comment = serializer.save()
            comment.author = request.user.my_user
            comment.save()
            comment_picture = CommentPicture.objects.create(comment=comment,
                                                            picture=serializer.validated_data['picture'])

            value = {
                'comment_pk': comment.pk,
                'picture_pk': comment_picture.pk,
                'picture_path': comment_picture.picture.path
            }

            return Response({'status': 'created', 'value': value},
                            status=status.HTTP_201_CREATED)


class CommentPicturesView(APIView):
    serializer_class = CommentPictureSerializer
    parser_class = (FileUploadParser,)

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        if not comment.author.user == request.user:
            return Response({'status': 'error'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CommentPictureSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            comment_picture = serializer.save()
            comment_picture.comment = comment
            comment_picture.save()

            value = {
                'picture_pk': comment_picture.pk,
                'picture_url': comment_picture.picture.url
            }

            return Response({'status': 'created', 'value': value},
                            status=status.HTTP_201_CREATED)


class CommentPictureView(APIView):
    def delete(self, request, picture_id):
        picture = get_object_or_404(CommentPicture, pk=picture_id)

        if not picture.comment.author.user == request.user:
            return Response({'status': 'error'}, status=status.HTTP_401_UNAUTHORIZED)

        picture.picture.delete(save=False)
        picture.delete()

        return Response({'status': 'deleted', 'message': 'Picture successfully deleted'})


class CommentRatesView(APIView):
    serializer_class = CommentRateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        if comment.author.user == request.user:
            return Response({'status': 'error', 'message': 'You cant rate your comment'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = CommentRateSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            comment_rate = serializer.save()
            comment_rate.comment = comment
            comment_rate.author = request.user.my_user

            try:
                comment_rate.save()
            except IntegrityError:
                return Response({'status': 'error', 'message': 'You already rated this comment'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

            if comment_rate.like:
                comment.rating += 1
            else:
                comment.rating -= 1

            comment.save()

            value = {
                'pk': comment_rate.pk,
                'like': comment_rate.like
            }

            return Response({'status': 'created', 'value': value}, status=status.HTTP_201_CREATED)


class CommentRateView(APIView):
    serializer_class = CommentRateSerializer

    def patch(self, request, rate_id):
        serializer = CommentRateSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            comment_rate = get_object_or_404(CommentRate, pk=rate_id)

            if not request.user == comment_rate.author.user:
                return Response({'status': 'error'}, status=status.HTTP_401_UNAUTHORIZED)

            new_comment_rate = serializer.save()
            if new_comment_rate.like == comment_rate.like:
                return Response({'status': 'ok'})
            else:
                comment_rate.like = new_comment_rate.like
                comment = comment_rate.comment
                if comment_rate.like:
                    if comment_rate.like:
                        comment.rating += 1
                    else:
                        comment.rating -= 1

                comment.save()
                comment_rate.save()

                return Response({'status': 'patched'})

    def delete(self, request, rate_id):
        comment_rate = get_object_or_404(CommentRate, pk=rate_id)

        if not request.user == comment_rate.author.user:
            return Response({'status': 'error'}, status=status.HTTP_401_UNAUTHORIZED)

        comment = comment_rate.comment
        if comment_rate.like:
            comment.rating += 1
        else:
            comment.rating -= 1

        comment.save()
        comment_rate.delete()

        return Response({'status': 'deleted'})


class BookmarksView(APIView):
    serializer_class = BookmarkSerializer

    def post(self, request):
        serializer = BookmarkSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            if not request.user.is_authenticated:
                return Response({'status': 'error'}, status=status.HTTP_401_UNAUTHORIZED)

            bookmark = Bookmark.objects.create(post=serializer.validated_data['post'],
                                               my_user=request.user.my_user)

            return Response({'status': 'created', 'value': {'pk': bookmark.pk}},
                            status=status.HTTP_201_CREATED)


class BookmarkView(APIView):
    def delete(self, request, bookmark_id):
        bookmark = get_object_or_404(Bookmark, pk=bookmark_id)

        if not request.user == bookmark.my_user.user:
            return Response({'status': 'error'}, status=status.HTTP_401_UNAUTHORIZED)

        bookmark.delete()

        return Response({'status': 'deleted', 'message': 'Bookmark successfully deleted'})
