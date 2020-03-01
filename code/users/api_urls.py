from django.urls import path

from .views import SingUpView, LoginView, CommentsView


urlpatterns = [
    path('sing-up/', SingUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('comments/', CommentsView.as_view())
]
