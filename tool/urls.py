from django.urls import path

from tool.views import display_index, upload_image, api_image_view, contact

app_name = 'tool'

urlpatterns = [
    path('', display_index, name='index'),
    path('api/images', api_image_view, name='api-view'),
    path('upload/batch/<str:batch>', upload_image, name='upload'),
    path('contact', contact, name='contact'),
]