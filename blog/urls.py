from django.urls import path
from . import views

app_name='blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('page/<int:page>/', views.page_list, name='list'),
    path('<slug:url_name>/', views.detail, name='detail'),
]
