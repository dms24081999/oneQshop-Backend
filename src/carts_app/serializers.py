from rest_framework import serializers
from .models import *
import json


class CartSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user_id", "product_id", "count", "ratings", "is_deleted"]
