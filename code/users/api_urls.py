from django.urls import path

from .views import SingUpView, LoginView, CommentsView, CommentView, CommentsPhotosView, CommentPhotosView


urlpatterns = [
    path('', SingUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('comments/', CommentsView.as_view()),
    path('comments/photos/', CommentsPhotosView.as_view()),
    path('comments/<int:comment_id>/', CommentView.as_view()),
    path('comments/<int:comment_id>/photos/', CommentPhotosView.as_view()),
]
