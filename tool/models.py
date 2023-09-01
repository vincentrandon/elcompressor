from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

from tool.helpers import CompressImage


# Create your models here.
class ImageUpload(models.Model):
    """ Class designed to create images. """
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    size = models.FloatField(blank=True, null=True)
    size_after_compression = models.FloatField(blank=True, null=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    download_link = models.CharField(max_length=255, blank=True, null=True)
    batch = models.CharField(max_length=255, blank=True, null=True)
    anonymous_upload = models.BooleanField(default=False)
    session_key = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return self.title

    def compression_percentage(self):
        if self.size:
            return round(((self.size / self.size_after_compression) / self.size) * 100, 2)
        else:
            return 0

    def save(self, *args, **kwargs):
        self.title = self.image.name
        self.size = self.image.size
        print(f'Image size before compression: {self.size / 1000000}MB')
        img = Image.open(self.image)
        img_format = img.format
        self.image = CompressImage(self.image, self.title, img_format).compress()
        self.size_after_compression = self.image.size
        print(f'Image size after compression: {self.size_after_compression / 1000000}MB')
        self.download_link = self.image.url
        super().save(*args, **kwargs)
