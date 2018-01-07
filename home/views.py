from django.shortcuts import render

def default(request):
    return home(request)
    #return debug(request)

def debug(request):
    return render(request, 'home/sample.html')

def home(request):
    return render(request, 'home/index.html')
