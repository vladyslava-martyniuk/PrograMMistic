from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user']
    list_filter = ['user']

    search_fields = ['title', 'content']


admin.site.register(Post, PostAdmin)
# Register your models here.
