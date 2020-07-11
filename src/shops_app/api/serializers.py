from rest_framework import serializers
from ..models import Shops, ShopProducts
from products_app.models import Products
from products_app.api.serializers import ProductsSerializer


class ShopsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Shops
        fields = [
            "id",
            "name",
            "address",
            "city_name",
            "pincode",
            "state_name",
            "country_name",
        ]


class ShopProductsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    product_details = serializers.SerializerMethodField("get_product_details")
    shop_details = serializers.SerializerMethodField("get_shop_detials")

    class Meta:
        model = ShopProducts
        fields = ["id", "product", "product_details", "shop", "shop_details"]

    def get_product_details(self, obj):
        serial = ProductsSerializer(Products.objects.get(pk=obj.product.pk))
        return serial.data

    def get_shop_detials(self, obj):
        serial = ShopsSerializer(Shops.objects.get(pk=obj.shop.pk))
        return serial.data
