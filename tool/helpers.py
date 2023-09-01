from io import BytesIO
import pngquant
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.fields.files import ImageFieldFile


class CompressImage:
    def __init__(self, image: ImageFieldFile, img_name: str, img_format: str) -> None:
        self.image = image
        self.img_name = img_name
        self.img_format = img_format

    def _open_image(self) -> Image:
        return Image.open(self.image)

    def _save_image(self, img: Image, **kwargs) -> InMemoryUploadedFile:
        buffer = BytesIO()
        img.save(buffer, format=self.img_format, **kwargs)
        buffer.seek(0)
        return InMemoryUploadedFile(
            buffer,
            'ImageField',
            self.img_name,
            f'image/{self.img_format.lower()}',
            buffer.__sizeof__(),
            None
        )

    def _manage_png(self) -> InMemoryUploadedFile:
        img = self._open_image()
        img.resize((img.width, img.height), resample=Image.LANCZOS)
        return self._save_image(img, optimize=True, quality=50)

    def _manage_jpg(self) -> InMemoryUploadedFile:
        img = self._open_image()
        return self._save_image(img, quality=50)

    def _manage_jpeg(self) -> InMemoryUploadedFile:
        img = self._open_image()
        return self._save_image(img, quality=50)

    def _manage_gif(self) -> InMemoryUploadedFile:
        img = self._open_image()
        return self._save_image(img)

    def compress(self) -> InMemoryUploadedFile:
        handler = getattr(self, f'_manage_{self.img_format.lower()}', None)
        if handler is None:
            raise ValueError('Image format not supported')
        return handler()




