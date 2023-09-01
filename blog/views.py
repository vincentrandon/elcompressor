from django.http import HttpRequest
from django.shortcuts import render

from blog.models import BlogPost


# Create your views here.
def blog_post(request: HttpRequest, slug: str) -> render:
    blog_post = BlogPost.objects.get(slug=slug)
    return render(request, 'blog/blog-post.html', {'blog_post': blog_post})