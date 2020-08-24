from django.urls import path

from .views import (
    SingUpView,
    LoginView,
    CommentsView,
    CommentView,
    CommentsPhotosView,
    CommentPicturesView,
    CommentPictureView,
    CommentRatesView,
    CommentRateView,
    BookmarksView,
    BookmarkView,
)


urlpatterns = [
    path('users/', SingUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('comments/', CommentsView.as_view(), name='api/comments'),
    path('comments/pictures/', CommentsPhotosView.as_view(), name='api/comments/pictures'),
    path('comments/pictures/<int:picture_id>/', CommentPictureView.as_view(), name='api/comment/picture'),
    path('comments/<int:comment_id>/', CommentView.as_view(), name='api/comment'),
    path('comments/<int:comment_id>/photos/', CommentPicturesView.as_view(), name='api/comment/pictures'),
    path('comments/<int:comment_id>/rates/', CommentRatesView.as_view(), name='api/comment/rates'),
    path('comments/rates/<int:rate_id>/', CommentRateView.as_view(), name='api/comment/rate'),
    path('bookmarks/', BookmarksView.as_view(), name='api/bookmarks'),
    path('bookmarks/<int:bookmark_id>', BookmarkView.as_view(), name='api/bookmark'),
]
