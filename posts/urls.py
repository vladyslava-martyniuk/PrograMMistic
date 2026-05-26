from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.post_list, name='post_list'),
    path('posts/create/', views.post_create, name='post_create'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('api/posts/create/', views.api_create_post, name='api_create_post'),
    path('api/posts/<int:post_id>/edit/', views.api_update_post, name='api_update_post'),
    path('api/posts/<int:post_id>/delete/', views.api_delete_post, name='api_delete_post'),
]
