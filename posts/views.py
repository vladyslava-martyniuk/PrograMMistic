import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .forms import PostForm
from .models import Post


def _request_data(request):
    if (request.content_type or '').startswith('application/json'):
        try:
            return json.loads(request.body.decode('utf-8')) if request.body else {}
        except json.JSONDecodeError:
            return {}
    return request.POST


def _can_change_post(user, post):
    return user.is_authenticated and (post.user == user or user.is_superuser)


def post_list(request):
    query = request.GET.get('search', '')
    posts = Post.objects.all().select_related('user').order_by('-created_at')

    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    return render(request, 'post_list.html', {'posts': posts, 'query': query})


main_feed = post_list


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()

    return render(request, 'post_form.html', {'form': form, 'title': 'Створення поста', 'button_text': 'Створити'})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if not _can_change_post(request.user, post):
        return redirect('post_list')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)

    return render(request, 'post_form.html', {'form': form, 'title': 'Редагування поста', 'button_text': 'Зберегти'})


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if _can_change_post(request.user, post) and request.method == 'POST':
        post.delete()

    return redirect('post_list')


@csrf_exempt
@require_http_methods(['POST'])
def api_create_post(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Потрібна авторизація'}, status=401)

    data = _request_data(request)
    title = (data.get('title') or '').strip()
    content = (data.get('content') or '').strip()

    if not title or not content:
        return JsonResponse({'error': 'Заповніть заголовок і текст поста'}, status=400)

    post = Post.objects.create(title=title, content=content, user=request.user)

    return JsonResponse({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'user': post.user.username,
        'created_at': post.created_at.isoformat(),
    }, status=201)


@csrf_exempt
@require_http_methods(['POST', 'PUT', 'PATCH'])
def api_update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if not _can_change_post(request.user, post):
        return JsonResponse({'error': 'Немає доступу'}, status=403)

    data = _request_data(request)
    title = (data.get('title') or post.title).strip()
    content = (data.get('content') or post.content).strip()

    if not title or not content:
        return JsonResponse({'error': 'Заповніть заголовок і текст поста'}, status=400)

    post.title = title
    post.content = content
    post.save()

    return JsonResponse({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'user': post.user.username,
        'created_at': post.created_at.isoformat(),
    })


@csrf_exempt
@require_http_methods(['POST', 'DELETE'])
def api_delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if not _can_change_post(request.user, post):
        return JsonResponse({'error': 'Немає доступу'}, status=403)

    post.delete()

    return JsonResponse({'deleted': True})
