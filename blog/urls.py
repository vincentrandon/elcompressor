from django.urls import path

from blog.views import blog_post

app_name = 'blog'

urlpatterns = [
    path('<str:slug>', blog_post, name='blog-post'),
    ]