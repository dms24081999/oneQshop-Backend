from rest_framework import serializers
from .models import *
import json
from django.core.exceptions import ObjectDoesNotExist


class BrandsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Brands
        fields = ["id", "name", "description", "is_deleted"]


class CategoriesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Categories
        fields = ["id", "name", "description", "image", "is_deleted"]


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
    cart_details = serializers.SerializerMethodField("get_cart_details", read_only=True)

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
            "cart_details",
            "is_deleted",
        ]

    def get_images_details(self, obj):
        serial = ProductImagesSerializer(
            ProductImages.objects.filter(id__in=obj.images.all()), many=True
        )
        return serial.data

    def get_categories_details(self, obj):
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

    def get_cart_details(self, obj):
        try:
            serial = CartsMiniSerializer(
                Carts.objects.get(
                    user_id=self.context["request"].user.id, product_id=obj.id
                )
            )
            return serial.data
        except ObjectDoesNotExist:
            return []


class CartsMiniSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Carts
        fields = ["id", "count", "ratings", "is_deleted"]


class CartsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    cart_details = serializers.SerializerMethodField("get_cart_details", read_only=True)

    class Meta:
        model = Carts
        fields = [
            "id",
            "cart_details",
            "user_id",
            "product_id",
            "count",
            "ratings",
            "is_deleted",
        ]

    def create(self, validated_data):
        user_id = validated_data.get("user_id", None)
        product_id = validated_data.get("product_id", None)
        if user_id is not None:
            data = Carts.objects.get(user_id=user_id, product_id=product_id)
            if data is not None:
                data.count = validated_data.get("count", data.count)
                data.save()
                return data
        data = Carts.objects.create(**validated_data)
        return data

    def get_cart_details(self, obj):
        try:
            serial = ProductsSerializer(
                Products.objects.get(id=obj.product_id.id), context=self.context
            )
            return serial.data
        except ObjectDoesNotExist:
            return []


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"
