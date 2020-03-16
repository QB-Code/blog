from django.contrib import admin

from .models import MyUser, Comment, CommentPhoto


admin.site.register(MyUser)
admin.site.register(Comment)
admin.site.register(CommentPhoto)
