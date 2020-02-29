from django.urls import path

from .views import SingUpView, LoginView


urlpatterns = [
    path('sing-up', SingUpView.as_view()),
    path('login', LoginView.as_view()),
]
