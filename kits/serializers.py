from rest_framework import serializers
from .models import Kit


class KitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kit
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "image_path",
            "samples",
            "created_at",
            "updated_at",
        ]