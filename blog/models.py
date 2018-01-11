from django.conf import settings
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.db import models
from django.urls import reverse

from .managers import BlogUserManager

class BlogUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=125, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = BlogUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def __unicode(self):
        return self.__str__()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

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
