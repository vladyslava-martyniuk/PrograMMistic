from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Post

def main_feed(request):
    query = request.GET.get('search', '')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')
        
    return render(request, 'feed.html', {'posts': posts, 'query': query})

def like_post(request, post_id):
    if request.method == "POST" and request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        return JsonResponse({'liked': liked, 'total_likes': post.likes.count()})
    return JsonResponse({'status': 'error'}, status=403)