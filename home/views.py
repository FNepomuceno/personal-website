from django.shortcuts import render, redirect, reverse

def default(request):
    return index(request)
    #return debug(request)

def index(request):
    return render(request, 'home/index.html')

def debug(request):
    return render(request, 'home/sample.html')

def home(request):
    return redirect(reverse('home:default'))

def blog(request):
    return redirect(reverse('blog:index'))
