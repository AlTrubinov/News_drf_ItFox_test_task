from django.contrib import admin
from .models import News, Comment, Like

admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Like)
