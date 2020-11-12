from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from mainsite.storage_backends import ProfilePrictureStorage
from django.core.files.storage import FileSystemStorage
from django.core.validators import RegexValidator
from django.utils import timezone
from . import crypto
from .settings import CONSTANTS, knox_settings
from django.utils.translation import gettext_lazy as _
from .tokens import get_token_generator
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.urls import reverse
from .signals import reset_password_token_created
from django.core.mail import send_mail
from decouple import config


TOKEN_GENERATOR_CLASS = get_token_generator()


# Create your models here.
class Users(AbstractBaseUser):
    first_name = models.CharField(
        db_column="first_name", max_length=255, blank=True, null=False
    )
    last_name = models.CharField(
        db_column="last_name", max_length=255, blank=True, null=False
    )
    email = models.EmailField(
        db_column="email",
        verbose_name="email address",
        max_length=255,
        unique=True,
        null=False,
        blank=False,
    )
    username = models.CharField(
        db_column="username", max_length=255, unique=True, null=False, blank=False
    )
    phone_regex = RegexValidator(
        regex=r"^\+91\d{10}$",
        message="Phone number must be entered in the format: '+919876543210'.",
    )  # ^\+91\d{10}$
    phone_number = models.CharField(
        validators=[phone_regex], max_length=14, blank=True, null=True
    )  # validators should be a list
    if not settings.AWS:
        picture = models.FileField(
            storage=FileSystemStorage(),
            upload_to=settings.AWS_PUBLIC_MEDIA_LOCATION + "/profile_picture/",
            db_column="picture",
            null=True,
            blank=True,
        )
    else:
        picture = models.FileField(
            storage=ProfilePrictureStorage(), db_column="picture", null=True, blank=True
        )
    active = models.BooleanField(default=True, db_column="active")
    staff = models.BooleanField(
        default=False, db_column="staff"
    )  # a admin user; non super-user
    admin = models.BooleanField(default=False, db_column="admin")  # a superuser
    all_logout = models.CharField(
        max_length=20, default="", null=True, blank=True, db_column="all_logout"
    )
    is_deleted = models.BooleanField(default=False)
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]  # username & Password are required by default.

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "users"

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):
        return "(" + str(self.pk) + ") " + self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active


class Addresses(models.Model):
    address = models.TextField(max_length=500)
    city_name = models.CharField(max_length=200, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    state_name = models.CharField(max_length=165, blank=True, null=True)
    country_name = models.CharField(max_length=40, unique=True, blank=True)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        db_table = "addresses"


class AuthTokenManager(models.Manager):
    def create(self, user, expiry=knox_settings.TOKEN_TTL):
        token = crypto.create_token_string()
        digest = crypto.hash_token(token)
        if expiry is not None:
            expiry = timezone.now() + expiry
        instance = super(AuthTokenManager, self).create(
            token_key=token[: CONSTANTS.TOKEN_KEY_LENGTH],
            digest=digest,
            user=user,
            expiry=expiry,
        )
        return instance, token


class AuthToken(models.Model):
    objects = AuthTokenManager()
    digest = models.CharField(max_length=CONSTANTS.DIGEST_LENGTH, primary_key=True)
    token_key = models.CharField(max_length=CONSTANTS.TOKEN_KEY_LENGTH, db_index=True)
    user = models.ForeignKey(
        Users,
        null=False,
        blank=False,
        related_name="auth_token_set",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "%s : %s" % (self.digest, self.user)


class ResetPasswordToken(models.Model):
    class Meta:
        verbose_name = _("Password Reset Token")
        verbose_name_plural = _("Password Reset Tokens")

    @staticmethod
    def generate_key():
        return (
            TOKEN_GENERATOR_CLASS.generate_token()
        )  # generates a pseudo random code using os.urandom and binascii.hexlify

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        Users,
        related_name="password_reset_tokens",
        on_delete=models.CASCADE,
        verbose_name=_("The User which is associated to this password reset token"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("When was this token generated")
    )
    # Key field, though it is not the primary key of the model
    key = models.CharField(_("Key"), max_length=64, db_index=True, unique=True)
    ip_address = models.GenericIPAddressField(
        _("The IP address of this session"), default="", blank=True, null=True
    )
    user_agent = models.CharField(
        max_length=256, verbose_name=_("HTTP User Agent"), default="", blank=True
    )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ResetPasswordToken, self).save(*args, **kwargs)

    def __str__(self):
        return "Password reset token for user {user}".format(user=self.user)


def get_password_reset_token_expiry_time():  # get token validation time
    """
    Returns the password reset token expirty time in hours (default: 24)
    Set Django SETTINGS.DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME to overwrite this time
    :return: expiry time
    """
    return getattr(settings, "DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME", 24)


def get_password_reset_lookup_field():
    """
    Returns the password reset lookup field (default: email)
    Set Django SETTINGS.DJANGO_REST_LOOKUP_FIELD to overwrite this time
    :return: lookup field
    """
    return getattr(settings, "DJANGO_REST_LOOKUP_FIELD", "email")


def clear_expired(expiry_time):
    """
    Remove all expired tokens
    :param expiry_time: Token expiration time
    """
    ResetPasswordToken.objects.filter(created_at__lte=expiry_time).delete()


def eligible_for_reset(self):
    if not self.is_active:  # if the user is active we dont bother checking
        return False
    if getattr(
        settings, "DJANGO_REST_MULTITOKENAUTH_REQUIRE_USABLE_PASSWORD", True
    ):  # if we require a usable password then return the result of has_usable_password()
        return self.has_usable_password()
    else:  # otherwise return True because we dont care about the result of has_usable_password()
        return True


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    email_plaintext_message = "{hosted_url}{reset_password_url}?token={reset_password_token}".format(
        hosted_url=config("HOSTED_URL"),
        reset_password_url=reverse("reset-password-request"),
        reset_password_token=reset_password_token.key,
    )
    send_mail(
        # title:
        "Password Reset for {title}".format(title="one-Q-shop"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@oneQshop.com",
        # to:
        [reset_password_token.user.email],
    )


# add eligible_for_reset to the user class
Users.add_to_class("eligible_for_reset", eligible_for_reset)


"""
Password Reset Token:

Copy link which is in email, will be similar to /api/password_reset/?token=339e80fe05e5ca9fc74799213f81a093d1f
Learn How to send Email in Django – Link
Now copy that token which comes in email and and post token and password to /api/password_reset/confirm/ api url.
{
    "token":"3339e80fe05e5ca9fc74799213f81a093d1f",
    "password":"Password@123"
}
"""
