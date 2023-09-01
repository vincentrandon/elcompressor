from rest_framework import serializers

from tool.models import ImageUpload


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = '__all__'