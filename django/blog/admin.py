from django.contrib import admin
from .models import Tag, Post, Comment  # Tag, Post, Comment class import


admin.site.register(Tag)  # admin 사이트에 Tag 모델을 등록(register)한다
admin.site.register(Post)  # admin 사이트에 Post 모델을 등록(register)한다
admin.site.register(Comment)  # admin 사이트에 Comment 모델을 등록(register)한다
