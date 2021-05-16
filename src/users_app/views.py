from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, GenericAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils import timezone
from rest_framework import status
from rest_framework.serializers import DateTimeField
from rest_framework.settings import api_settings
from .auth import TokenAuthentication
from .models import AuthToken
from .settings import knox_settings
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer

from datetime import timedelta
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import (
    validate_password,
    get_password_validators,
)
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from rest_framework import status, exceptions
from .signals import *
from decouple import config


Users = get_user_model()


class LoginView(APIView):
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = (AllowAny,)

    def get_context(self):
        return {"request": self.request, "format": self.format_kwarg, "view": self}

    def get_token_ttl(self):
        return knox_settings.TOKEN_TTL

    def get_token_limit_per_user(self):
        return knox_settings.TOKEN_LIMIT_PER_USER

    def get_user_serializer_class(self):
        return knox_settings.USER_SERIALIZER

    def get_expiry_datetime_format(self):
        return knox_settings.EXPIRY_DATETIME_FORMAT

    def format_expiry_datetime(self, expiry):
        datetime_format = self.get_expiry_datetime_format()
        return DateTimeField(format=datetime_format).to_representation(expiry)

    def get_post_response_data(self, request, token, instance):
        data = {"expiry": self.format_expiry_datetime(instance.expiry), "token": token}
        data["user"] = UsersSerializer(request.user, context=self.get_context()).data
        return data

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        token_limit_per_user = self.get_token_limit_per_user()
        if token_limit_per_user is not None:
            now = timezone.now()
            token = request.user.auth_token_set.filter(expiry__gt=now)
            if token.count() >= token_limit_per_user:
                return Response(
                    {"error": "Maximum amount of tokens allowed per user exceeded."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        token_ttl = self.get_token_ttl()
        instance, token = AuthToken.objects.create(request.user, token_ttl)
        user_logged_in.send(
            sender=request.user.__class__, request=request, user=request.user
        )
        data = self.get_post_response_data(request, token, instance)
        return Response(data)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        request._auth.delete()
        user_logged_out.send(
            sender=request.user.__class__, request=request, user=request.user
        )
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class LogoutAllView(APIView):
    """
    Log the user out of all sessions
    I.E. deletes all auth tokens for the user
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        request.user.auth_token_set.all().delete()
        user_logged_out.send(
            sender=request.user.__class__, request=request, user=request.user
        )
        return Response(None, status=status.HTTP_204_NO_CONTENT)


# __all__ = [
#     'ResetPasswordValidateToken',
#     'ResetPasswordConfirm',
#     'ResetPasswordRequestToken',
#     'reset_password_validate_token',
#     'reset_password_confirm',
#     'reset_password_request_token'
# ]

HTTP_USER_AGENT_HEADER = getattr(
    settings, "DJANGO_REST_PASSWORDRESET_HTTP_USER_AGENT_HEADER", "HTTP_USER_AGENT"
)
HTTP_IP_ADDRESS_HEADER = getattr(
    settings, "DJANGO_REST_PASSWORDRESET_IP_ADDRESS_HEADER", "REMOTE_ADDR"
)


class ResetPasswordValidateToken(
    GenericAPIView
):  # An Api View which provides a method to verify that a token is valid
    throttle_classes = ()
    permission_classes = ()
    serializer_class = ResetTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"status": "OK"})


class ResetPasswordConfirm(
    GenericAPIView
):  # An Api View which provides a method to reset a password based on a unique token
    throttle_classes = ()
    permission_classes = ()
    serializer_class = PasswordTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data["password"]
        token = serializer.validated_data["token"]
        reset_password_token = ResetPasswordToken.objects.filter(
            key=token
        ).first()  # find token
        if (
            reset_password_token.user.eligible_for_reset()
        ):  # change users password (if we got to this code it means that the user is_active)
            pre_password_reset.send(
                sender=self.__class__, user=reset_password_token.user
            )
            try:
                validate_password(
                    password,
                    user=reset_password_token.user,
                    password_validators=get_password_validators(
                        settings.AUTH_PASSWORD_VALIDATORS
                    ),
                )  # validate the password against existing validators
            except ValidationError as e:
                raise exceptions.ValidationError(
                    {"password": e.messages}
                )  # raise a validation error for the serializer
            reset_password_token.user.set_password(password)
            reset_password_token.user.save()
            post_password_reset.send(
                sender=self.__class__, user=reset_password_token.user
            )
        ResetPasswordToken.objects.filter(
            user=reset_password_token.user
        ).delete()  # Delete all password reset tokens for this user
        return Response({"status": "OK"})


class ResetPasswordRequestToken(
    GenericAPIView
):  # An Api View which provides a method to request a password reset token based on an e-mail address. Sends a signal reset_password_token_created when a reset token was created
    throttle_classes = ()
    permission_classes = ()
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password_reset_token_validation_time = (
            get_password_reset_token_expiry_time()
        )  # before we continue, delete all existing expired tokens
        now_minus_expiry_time = timezone.now() - timedelta(
            hours=password_reset_token_validation_time
        )  # datetime.now minus expiry hours
        clear_expired(
            now_minus_expiry_time
        )  # delete all tokens where created_at < now - 24 hours
        users = Users.objects.filter(
            **{"{}__iexact".format(get_password_reset_lookup_field()): email}
        )  # find a user by email address (case insensitive search)
        active_user_found = False
        # iterate over all users and check if there is any user that is active
        # also check whether the password can be changed (is useable), as there could be users that are not allowed to change their password (e.g., LDAP user)
        for user in users:
            if user.eligible_for_reset():
                active_user_found = True
        # No active user found, raise a validation error but not if DJANGO_REST_PASSWORDRESET_NO_INFORMATION_LEAKAGE == True
        if not active_user_found and not getattr(
            settings, "DJANGO_REST_PASSWORDRESET_NO_INFORMATION_LEAKAGE", False
        ):
            raise exceptions.ValidationError(
                {
                    "email": [
                        _(
                            "We couldn't find an account associated with that email. Please try a different e-mail address."
                        )
                    ]
                }
            )

        # last but not least: iterate over all users that are active and can change their password and create a Reset Password Token and send a signal with the created token
        for user in users:
            if user.eligible_for_reset():
                token = None  # define the token as none for now
                if (
                    user.password_reset_tokens.all().count() > 0
                ):  # check if the user already has a token
                    token = user.password_reset_tokens.all()[
                        0
                    ]  # yes, already has a token, re-use this token
                else:
                    token = ResetPasswordToken.objects.create(
                        user=user,
                        user_agent=request.META.get(HTTP_USER_AGENT_HEADER, ""),
                        ip_address=request.META.get(HTTP_IP_ADDRESS_HEADER, ""),
                    )  # no token exists, generate a new token
                # send a signal that the password token was created let whoever receives this signal handle sending the email for the password reset
                reset_password_token_created.send(
                    sender=self.__class__, instance=self, reset_password_token=token
                )
        return Response({"status": "OK"})


class UsersCreateInfoAPIView(CreateAPIView):
    serializer_class = UsersCreateSerializer
    permission_classes = [AllowAny]
    queryset = Users.objects.all()

    def get_token_ttl(self):
        return knox_settings.TOKEN_TTL

    def get_expiry_datetime_format(self):
        return knox_settings.EXPIRY_DATETIME_FORMAT

    def format_expiry_datetime(self, expiry):
        datetime_format = self.get_expiry_datetime_format()
        return DateTimeField(format=datetime_format).to_representation(expiry)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        serializerData = UsersSerializer(
            user, context=self.get_serializer_context()
        ).data
        print("Register user pk: ", user.pk)
        serializerData["current_user"] = user.pk
        token_ttl = self.get_token_ttl()
        instance, token = AuthToken.objects.create(user, token_ttl)
        return Response(
            {
                "user": serializerData,
                "token": token,
                "expiry": self.format_expiry_datetime(instance.expiry),
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class ChangePasswordAPIView(UpdateAPIView):  # """An endpoint for changing password."""

    serializer_class = ChangePasswordSerializer
    model = Users
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if serializer.data.get("old_password") == serializer.data.get(
                "new_password"
            ):
                return Response(
                    {"new_password": ["New Password can't be Old Password!"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersIsAuthenticatedAPIView(GenericAPIView):
    serializer_class = UsersSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        context = super(UsersIsAuthenticatedAPIView, self).get_serializer_context()
        context.update(
            {
                "request": self.request
                # extra data
            }
        )
        return context

    # GET
    def get(self, request, *args, **kwargs):
        print("current pk", request.user.pk)
        if not request.user.is_authenticated:
            return Response({"detail": "Auth not provided."}, status=400)
        else:
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)


class UsersFullInfoAPIView(ModelViewSet):
    lookup_field = "pk"
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Users.objects.all()

    # List GET
    def get_queryset(self, *args, **kwargs):
        context = super(UsersFullInfoAPIView, self).get_queryset(*args, **kwargs)
        qs = self.queryset
        query = self.request.GET.get("s")
        if query is not None:
            qs = qs.filter(
                Q(username__icontains=query)
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
            ).distinct()
        return qs

    # GET
    def retrieve(self, request, pk, *args, **kwargs):
        print("current pk", pk, request.user.pk)
        if not request.user.is_authenticated:
            return Response({"detail": "Auth not provided."}, status=400)
        # elif int(pk)!=int(request.user.pk):
        #     return Response({"detail": "Not found."}, status=400)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

    # PUT
    def update(self, request, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Auth not provided."}, status=400)
        elif int(pk) != int(request.user.pk):
            return Response({"detail": "Not found."}, status=400)
        else:
            partial = kwargs.pop("partial", False)
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

    # PATCH
    def partial_update(self, request, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Auth not provided."}, status=400)
        elif int(pk) != int(request.user.pk):
            return Response({"detail": "Not found."}, status=400)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

    # DELETE
    def destroy(self, request, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Auth not provided."}, status=400)
        elif int(pk) != int(request.user.pk):
            return Response({"detail": "Not found."}, status=400)
        else:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
