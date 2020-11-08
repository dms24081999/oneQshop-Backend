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
