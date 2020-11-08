from rest_framework import serializers

from django.contrib.auth import get_user_model

Users = get_user_model()


class ChangePasswordSerializer(serializers.Serializer):
    model = Users
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UsersCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Users
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password",
            "picture",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = Users.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UsersSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    current_user = serializers.SerializerMethodField("curruser")
    picture_path = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Users
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "current_user",
            "picture",
            "picture_path",
        ]

    def curruser(self, obj):
        try:
            # print(self.context["request"].user.id)
            return self.context["request"].user.id
        except:
            pass

    def get_picture_path(self, obj):
        request = self.context.get("request")
        try:
            return obj.picture.url
        except:
            return None
        # return request.build_absolute_uri(photo_url)
