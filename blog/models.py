from django.conf import settings
from django.db import models
from django.urls import reverse

class Post(models.Model):
    # Main Content
    title = models.CharField(max_length=125)
    content = models.TextField()

    # Meta Data
    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE,
        default=1)
    url_name = models.SlugField(unique=True, default='null')

    # Time Created/Updated
    time_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.__str__

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'url_name':self.url_name})

    class Meta:
        ordering = ["-time_created", "-last_updated"]
