from django.urls import path
from . import views

app_name='blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:url_name>/', views.post_detail, name='detail'),
    # path('page/<int:page>/', views.page_list, name='list'),
]

