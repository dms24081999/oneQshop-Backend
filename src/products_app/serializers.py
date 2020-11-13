from rest_framework import serializers
from .models import *
import json


class BrandsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Brands
        fields = ["id", "name", "description", "is_deleted"]


class CategoriesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Categories
        fields = ["id", "name", "description", "is_deleted"]


class ProductImagesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ProductImages
        fields = ["id", "image", "main_image", "is_deleted"]


class ProductsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    images_details = serializers.SerializerMethodField(
        "get_images_details", read_only=True
    )
    categories_details = serializers.SerializerMethodField(
        "get_categories_details", read_only=True
    )
    brand_details = serializers.SerializerMethodField(
        "get_brand_details", read_only=True
    )

    class Meta:
        model = Products
        fields = [
            "id",
            "barcode",
            "name",
            "categories_details",
            "brand_details",
            "images_details",
            "price",
            "is_deleted",
        ]

    def get_images_details(self, obj):
        serial = ProductImagesSerializer(
            ProductImages.objects.filter(id__in=obj.images.all()), many=True
        )
        return serial.data

    def get_categories_details(self, obj):
        # serial = CategoriesSerializer(Categories.objects.get(id=obj.category.id))
        serial = CategoriesSerializer(
            Categories.objects.filter(id__in=obj.categories.all()), many=True
        )
        return serial.data

    def get_brand_details(self, obj):
        if obj.brand:
            serial = BrandsSerializer(Brands.objects.get(id=obj.brand.id))
            return serial.data
        else:
            return None


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"
