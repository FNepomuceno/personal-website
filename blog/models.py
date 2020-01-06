from itertools import count
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django.urls import reverse


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


def get_unique_post_slug(title='null0', max_length=50):
    original_slug = slugify(title)[:max_length]
    slug = original_slug
    for x in count(1):
        if not Post.objects.filter(url_name=slug).exists():
            break
        slug = '{}-{}'.format(original_slug[:max_length-len(str(x))-1], x)
    return slug


class User(AbstractUser):
    pass


class Post(models.Model):
    title = models.CharField(max_length=125)
    content = models.TextField()

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        default=1
    )
    url_name = models.SlugField(unique=True, default=get_unique_post_slug)

    time_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'url_name':self.url_name})

    class Meta:
        ordering = ['-time_created', '-last_updated']
