from django.contrib import admin

from .models import MyUser, Comment, CommentPicture


admin.site.register(MyUser)
admin.site.register(Comment)
admin.site.register(CommentPicture)
