from rest_framework import serializers
from .models import *
import json
from products_app.models import *
from products_app.serializers import ProductsSerializer
from django.core.exceptions import ObjectDoesNotExist


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

    def get_cart_details(self, obj):
        try:
            serial = ProductsSerializer(Products.objects.get(id=obj.product_id.id))
            return serial.data
        except ObjectDoesNotExist:
            return []
