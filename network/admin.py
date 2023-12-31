from django.contrib import admin
from .models import User, Post, Like, Follower
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")

class PostAdmin(admin.ModelAdmin):
    list_display = ("owner", "timestamp", "content")

class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "post owner", "post content", "liked?")

class FollowerAdmin(admin.ModelAdmin):
    filter_horizontal = ("user", "follower",)


admin.site.register(User)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Follower)

