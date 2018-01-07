from django.urls import path
from . import views

app_name='home'
urlpatterns = [
    path('', views.default, name='default'),
    path('home/', views.home, name='home'),
]
