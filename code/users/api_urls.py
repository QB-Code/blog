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
    path('comments/', CommentsView.as_view(), name='api/comments'),
    path('comments/photos/', CommentsPhotosView.as_view(), name='api/comments/photos'),
    path('comments/photos/<int:photo_id>/', CommentPhotoView.as_view(), name='api/comments/photo'),
    path('comments/<int:comment_id>/', CommentView.as_view(), name='comment'),
    path('comments/<int:comment_id>/photos/', CommentPhotosView.as_view(), name='api/comment/photos'),
    path('comments/<int:comment_id>/rates/', CommentRatesView.as_view(), name='api/comment/rates'),
    path('comments/rates/<int:rate_id>/', CommentRateView.as_view(), name='api/comment/rate'),
    path('bookmarks/', BookmarksView.as_view(), name='api/bookmarks'),
    path('bookmarks/<int:bookmark_id>', BookmarkView.as_view(), name='api/bookmark'),
]
