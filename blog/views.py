from django.shortcuts import render, get_object_or_404
from .models import Post

def index(request):
    return post_list(request)


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'blog/list.html', context)


def post_detail(request, url_name=None):
    instance = get_object_or_404(Post, url_name=url_name)
    context = {
        'post': instance
    }
    return render(request, 'blog/detail.html', context)
