from django.contrib import admin
from .models import Post
from .forms import PostForm

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ["title", "last_updated", "time_created"]
    list_filter = ["last_updated", "time_created"]
    search_fields = ["title", "content"]

    def save_model(self, request, instance, form, change):
        instance.author = request.user
        super().save_model(request, instance, form, change)
