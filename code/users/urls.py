from django.urls import path
from django.contrib.auth.views import PasswordResetConfirmView, LogoutView

from .views import password_reset, user_page


urlpatterns = [
    path('<int:user_id>/', user_page, name='user_page'),
    path('logout/',  LogoutView.as_view(), name='logout'),
    path('password-reset', password_reset, name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm')
]