from itertools import count
from django import forms
from django.utils.text import slugify
from .models import Post

class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=125,
        widget=forms.TextInput(attrs={'class':'form-control'}))
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class':'form-control'}))

    def save(self, commit=True):
        instance = super(PostForm, self).save(commit=False)
        if not self.instance.pk:
            self.set_url_name(instance)
        return instance

    def set_url_name(self, instance):
        max_length = Post._meta.get_field('url_name').max_length
        instance.url_name = self.get_unique_slug(instance, max_length)
        instance.save()

    def get_unique_slug(self, instance, max_length):
        title = instance.title
        orig = slug = slugify(instance.title)[:max_length]
        for x in count(1):
            if not Post.objects.filter(url_name=slug).exists():
                break
            slug = "{}-{}".format(orig[:max_length-len(str(x))-1], x)
        return slug

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
        ]
