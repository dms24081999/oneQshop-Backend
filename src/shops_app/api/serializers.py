from rest_framework import serializers
from ..models import Shops


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
