from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_date = models.DateField(auto_now_add=True, null=True)
    blog_time = models.TimeField(null=True)
    title = models.CharField(max_length=64)
    content = models.TextField(max_length=4000)
    image = models.ImageField(null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    slug = models.SlugField(max_length=50, unique=True, null=False)

    class Meta:
        ordering = ['-blog_date', '-blog_time']

    def __str__(self):
        return f'Blog { self.content } by { self.author }'
