from django.urls import path
from .views import all_posts, uno_post, rubrics, write_post


urlpatterns = [
    path('', all_posts, name='all_posts'),
    path('posts/<int:post_id>/', uno_post, name='uno_post'),
    path('writing/<int:post_id>/', write_post, name='write_post'),
    path('rubrics/', rubrics, name='rubrics'),
]
