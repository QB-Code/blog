from django.urls import path

from .views import (
    SingUpView,
    LoginView,
    CommentsView,
    CommentView,
    CommentsPhotosView,
    CommentPhotosView,
    CommentPhotoView,
    CommentRatesView,
    CommentRateView,
    BookmarksView,
    BookmarkView,
)


urlpatterns = [
    path('users/', SingUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('comments/', CommentsView.as_view()),
    path('comments/photos/', CommentsPhotosView.as_view()),
    path('comments/photos/<int:photo_id>/', CommentPhotoView.as_view()),
    path('comments/<int:comment_id>/', CommentView.as_view()),
    path('comments/<int:comment_id>/photos/', CommentPhotosView.as_view()),
    path('comments/<int:comment_id>/rates/', CommentRatesView.as_view()),
    path('comments/rates/<int:rate_id>/', CommentRateView.as_view()),
    path('bookmarks/', BookmarksView.as_view()),
    path('bookmarks/<int:bookmark_id>', BookmarkView.as_view()),
]
