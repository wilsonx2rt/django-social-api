from django.contrib import admin

# Register your models here.
from project.feed.models import Post, UserProfile
from project.feed.models import Tags

class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'created']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user']

admin.site.register(Post)
admin.site.register(Tags)
admin.site.register(UserProfile, UserProfileAdmin)