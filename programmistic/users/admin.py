from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'bio']
    list_filter = ['id', 'user']

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'user']
    list_filter = ['title', 'content', 'user']
