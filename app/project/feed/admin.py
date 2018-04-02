from django.contrib import admin

# Register your models here.
from project.feed.models import Post, UserProfile, FriendRequests, Like
from project.feed.models import Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'created']


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user']


admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(FriendRequests)
admin.site.register(UserProfile, UserProfileAdmin)
