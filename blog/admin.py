from django.contrib import admin

from blog.models import BlogPost


# Register your models here.
class CustomBlogPost(admin.ModelAdmin):

    model = BlogPost
    list_display = ('title', 'author', 'date_posted')

admin.site.register(BlogPost, CustomBlogPost)