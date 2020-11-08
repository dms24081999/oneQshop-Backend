from rest_framework import serializers

from django.contrib.auth import get_user_model

from datetime import timedelta

from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404 as _get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import get_password_reset_token_expiry_time
from . import models

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


# __all__ = [
#     'EmailSerializer',
#     'PasswordTokenSerializer',
#     'ResetTokenSerializer',
# ]


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordValidateMixin:
    def validate(self, data):
        token = data.get("token")

        # get token validation time
        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        # find token
        try:
            reset_password_token = _get_object_or_404(
                models.ResetPasswordToken, key=token
            )
        except (
            TypeError,
            ValueError,
            ValidationError,
            Http404,
            models.ResetPasswordToken.DoesNotExist,
        ):
            raise Http404(
                _("The OTP password entered is not valid. Please check and try again.")
            )

        # check expiry date
        expiry_date = reset_password_token.created_at + timedelta(
            hours=password_reset_token_validation_time
        )

        if timezone.now() > expiry_date:
            # delete expired token
            reset_password_token.delete()
            raise Http404(_("The token has expired"))
        return data


class PasswordTokenSerializer(PasswordValidateMixin, serializers.Serializer):
    password = serializers.CharField(
        label=_("Password"), style={"input_type": "password"}
    )
    token = serializers.CharField()


class ResetTokenSerializer(PasswordValidateMixin, serializers.Serializer):
    token = serializers.CharField()
