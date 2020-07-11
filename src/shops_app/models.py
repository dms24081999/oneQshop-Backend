from django.db import models
from django.conf import settings

# Create your models here.


class Shops(models.Model):
    name = models.CharField(
        db_column="name", max_length=255, unique=True, null=False, blank=False
    )
    short_name = models.SlugField(
        db_column="short_name", max_length=255, null=False, blank=False
    )
    address = models.TextField(max_length=500)
    city_name = models.CharField(max_length=200, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    state_name = models.CharField(max_length=165, blank=True, null=True)
    country_name = models.CharField(max_length=40, unique=True, blank=True)

    class Meta:
        verbose_name = "Shop"
        verbose_name_plural = "Shops"
        db_table = "shops"
