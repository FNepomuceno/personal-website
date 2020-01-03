from django.shortcuts import render
from .models import Post

# Create your views here.
def index(request):
    return post_list(request)

def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'blog/list.html', context)
