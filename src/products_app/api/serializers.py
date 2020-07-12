from rest_framework import serializers
from ..models import Products, Categories, ProductImages
import json


class CategoriesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Categories
        fields = ["id", "name", "short_name", "description"]


class ProductImagesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ProductImages
        fields = ["id", "image", "main_image"]


class ProductsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    images_details = serializers.SerializerMethodField(
        "get_images_details", read_only=True
    )
    category_details = serializers.SerializerMethodField(
        "get_category_details", read_only=True
    )

    class Meta:
        model = Products
        fields = [
            "id",
            "barcode",
            "name",
            "short_name",
            "category",
            "category_details",
            "images",
            "images_details",
        ]

    def get_images_details(self, obj):
        serial = ProductImagesSerializer(
            ProductImages.objects.filter(id__in=obj.images.all()), many=True
        )
        return serial.data

    def get_category_details(self, obj):
        serial = CategoriesSerializer(Categories.objects.get(id=obj.category.id))
        return serial.data
