from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post

def index(request):
    return post_list(request)


def blog_login(request):
    username = request.POST['username']
    password = request.POST['password']
    next_url = request.POST['next']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Show success message?
        pass
    else:
        # Show error message?
        pass
    return redirect(next_url)


def blog_logout(request):
    logout(request)
    return redirect('/blog/')


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
        'user': request.user,
    }
    return render(request, 'blog/list.html', context)


def post_detail(request, url_name=None):
    post = get_object_or_404(Post, url_name=url_name)
    context = {
        'post': post,
        'user': request.user,
    }
    return render(request, 'blog/detail.html', context)
