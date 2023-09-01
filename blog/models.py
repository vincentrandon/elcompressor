from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from tinymce.models import HTMLField


# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    headline = models.TextField(null=True, blank=True, max_length=300)
    first_part_content = models.TextField(null=True, blank=True)
    second_part_content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='blog/images/', null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=300, unique=True, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog-post', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)