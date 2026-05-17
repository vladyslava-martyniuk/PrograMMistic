from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_feed, name='home'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
]