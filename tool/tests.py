import base64

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from accounts.models import User
from tool.models import ImageUpload


class TestUserCanUploadImage(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser@gmail.com',
            'email': 'testuser@gmail.com',
            'password': 'testpassword'
        }
        User.objects.create_user(**self.credentials)

    def test_user_upload_image(self):
        self.client.login(
            username=self.credentials['username'],
            password=self.credentials['password']
        )
        #Create dummy png file
        image = open('static/home/assets/compress_logotype.png', 'rb').read()
        img = SimpleUploadedFile(name='test_image.png', content=image, content_type='image/png')
        print(img)
        response = self.client.post('', {'images': img}, follow=True)
        #We check the image is in the database
        self.assertTrue(ImageUpload.objects.count(), 1)


class TestAnonymousUserCanUploadImage(TestCase):
    def test_anonymous_user_upload_image(self):
        # Create dummy png file
        image = open('static/home/assets/compress_logotype.png', 'rb').read()
        img = SimpleUploadedFile(name='test_image.png', content=image, content_type='image/png')
        response = self.client.post('', {'images': img}, follow=True)
        # We check the image is in the database
        self.assertTrue(ImageUpload.objects.count(), 1)


class TestAnonymousUserUploadImageIsLimitedto5(TestCase):
    def test_anonymous_user_upload_image_is_limited_to_5(self):
        # Create 5 dummy png files
        for i in range(5):
            image = open('static/home/assets/compress_logotype.png', 'rb').read()
            img = SimpleUploadedFile(name=f'test_image{i}.png', content=image, content_type='image/png')
            response = self.client.post('', {'images': img}, follow=True)
        # We check the image is in the database
        self.assertTrue(ImageUpload.objects.count(), 5)

    def test_anonymous_user_upload_image_is_limited_to_5_plus_one(self):
        # Create 5 dummy png files
        for i in range(5):
            image = open('static/home/assets/compress_logotype.png', 'rb').read()
            img = SimpleUploadedFile(name=f'test_image{i}.png', content=image, content_type='image/png')
            response = self.client.post('', {'images': img}, follow=True)
            print(ImageUpload.objects.get(id=i+1).session_key)
        # We check the image is in the database

        # Create 6th dummy png file
        image = open('static/home/assets/compress_logotype.png', 'rb').read()
        img = SimpleUploadedFile(name=f'test_image6.png', content=image, content_type='image/png')
        #if we try to upload a 6th image, we check the context contains the max_images variable
        response = self.client.post('', {'images': img}, follow=True)
        self.assertTrue(response.context['max_images'])
        print(f'Image count: {ImageUpload.objects.count()}')








