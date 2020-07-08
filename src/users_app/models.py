from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser
)
from .managers import (
    UserManager
)


# Create your models here.
class User(AbstractBaseUser):
    first_name = models.CharField(
        db_column="first_name", max_length=255, blank=True, null=False
    )
    last_name = models.CharField(
        db_column="last_name", max_length=255, blank=True, null=False
    )
    email = models.EmailField(
        db_column="email",
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=False,
        blank=False
    )
    username= models.TextField(
        db_column="username",
        max_length=255,
        unique=True,
        null=False,
        blank=False
    )
    active = models.BooleanField(default=True,db_column="active")
    staff = models.BooleanField(default=False,db_column="staff") # a admin user; non super-user
    admin = models.BooleanField(default=False,db_column="admin") # a superuser
    all_logout = models.CharField(max_length=20,default='',null=True,blank=True,db_column="all_logout")
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email'] # username & Password are required by default.

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):             
        return self.email

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