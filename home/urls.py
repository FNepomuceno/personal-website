from django.urls import path
from . import views

app_name='home'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('blog/', views.blog, name='blog'),
    path('', views.default, name='default'),
]
