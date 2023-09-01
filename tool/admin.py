from django.contrib import admin

from tool.models import ImageUpload


# Register your models here.
class ModelImageAdmin(admin.ModelAdmin):
    """ Class designed to create images. """
    model = ImageUpload
    list_display = ['title', 'image', 'id']

admin.site.register(ImageUpload, ModelImageAdmin)