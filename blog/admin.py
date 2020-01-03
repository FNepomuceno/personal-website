from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post
from .forms import PostForm

admin.site.register(User, UserAdmin)


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ['title', 'author', 'url_name',
        'last_updated', 'time_created']
    list_filter = ['last_updated', 'time_created']
    search_fields = ['title', 'content']

    def save_model(self, request, instance, form, change):
        instance.author = request.user
        super().save_model(request, instance, form, change)
