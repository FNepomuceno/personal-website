from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from .models import Post

def index(request):
    return page_list(request)

def page_list(request, page=1):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    posts = paginator.get_page(page)
    context = {
        'post_list': posts
    }
    return render(request, 'blog/list.html', context)

def detail(request, url_name=None):
    instance = get_object_or_404(Post, url_name=url_name)
    context = {
        'post': instance
    }
    return render(request, 'blog/detail.html', context)
