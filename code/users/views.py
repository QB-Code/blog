from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.views import Response

from .serializers import UserSerializer, LoginSerializer, CommentSerializer
from .models import MyUser
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
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = authenticate(request=request, **serializer.data)
            print(user)
            if user is not None:
                login(request=request, user=user)
                return Response({'status': 'ok', 'message': 'User successfully logged in'})
            else:
                return Response({'status': 'error', 'message': 'Username or password is incorrect'},
                                status=status.HTTP_400_BAD_REQUEST)


class CommentsView(APIView):
    def post(self, request):
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            if not request.user.is_authenticated:
                return Response({'status': 'error', 'message': 'User is not logged in'},
                                status=status.HTTP_401_UNAUTHORIZED)

            comment = serializer.save()
            comment.author = request.user.my_user
            comment.save()

            return Response({'status': 'created',
                             'value': serializer.data},
                            status=status.HTTP_201_CREATED)
