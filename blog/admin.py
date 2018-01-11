from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import Post, BlogUser
from .forms import PostForm, UserAddForm, UserChangeForm

@admin.register(BlogUser)
class UserAdmin(BaseUserAdmin):
    add_form = UserAddForm
    form = UserChangeForm
    list_display = ["username", "email", "date_joined", "is_admin"]
    list_filter = ["is_admin"]
    ordering = ["username"]
    search_fields = ["username", "email"]

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'pass_conf'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_admin')})
    )

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ["title", "last_updated", "time_created"]
    list_filter = ["last_updated", "time_created"]
    search_fields = ["title", "content"]

    def save_model(self, request, instance, form, change):
        instance.author = request.user
        super().save_model(request, instance, form, change)

admin.site.unregister(Group)
