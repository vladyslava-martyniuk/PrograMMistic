from django.contrib import admin

# Register your models here.
from .models import Profile
from posts.models import Post
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'avatar', 'post']
    list_filter = ['user', 'bio', 'avatar', 'post']

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'user']
    list_filter = ['title', 'content', 'user']
