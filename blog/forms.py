from itertools import count
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.text import slugify
from .models import Post, BlogUser

class UserAddForm(forms.ModelForm):
    password = forms.CharField(label='Password',
        widget=forms.PasswordInput)
    pass_conf = forms.CharField(label='Password confirmation',
        widget=forms.PasswordInput)

    class Meta:
        model = BlogUser
        fields = [
            'username',
            'email',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def clean_password2(self):
        pass_proposed = self.cleaned_data.get("password")
        pass_repeated = self.cleaned_data.get("pass_conf")
        if pass_proposed and pass_repeated and \
            pass_proposed != pass_repeated:
            raise ValidationError("Passwords don't match")
        return pass_repeated

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = BlogUser
        fields = [
            'username',
            'email',
            'password',
            'is_active',
            'is_admin',
        ]

    def clean_password(self):
        return self.initial["password"]

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
