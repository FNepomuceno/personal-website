from django.shortcuts import render

def index(request):
    return page_list(request)

def page_list(request, page=1):
    return render(request, 'blog/list.html')
