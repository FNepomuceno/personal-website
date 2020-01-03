from django import forms
from .models import Post, get_unique_post_slug


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=125,
        widget=forms.TextInput(attrs={'class':'form-control'}))
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class':'form-control'}))

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
        ]

    def save(self, commit=True):
        instance = super(PostForm, self).save(commit=False)
        if not self.instance.pk:
            self.set_url_name(instance)
        return instance

    def set_url_name(self, instance):
        max_length = Post._meta.get_field('url_name').max_length
        instance.url_name = get_unique_post_slug(instance.title, max_length)
        instance.save()
