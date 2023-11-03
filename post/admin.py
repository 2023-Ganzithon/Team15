from django.contrib import admin

from post.models import Post, Comment, Video

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Video)