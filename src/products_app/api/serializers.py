from rest_framework import serializers
from ..models import Products, Categories


class ProductsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Products
        fields = ["id", "barcode", "name", "short_name", "category"]


class CategoriesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Categories
        fields = ["id", "name", "short_name", "description"]
