from django.shortcuts import render
from django.contrib.auth.forms import PasswordResetForm


def user_page(request, user_id):
    return render(request, template_name='users/user.html')


def password_reset(request):
    return render(request, template_name='users/password-reset-confirm.html')

