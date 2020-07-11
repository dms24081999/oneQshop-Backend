from django.db import models
from django.conf import settings

from mainsite.storage_backends import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model

Users = get_user_model()


class Categories(models.Model):
    name = models.CharField(
        db_column="name", max_length=255, unique=True, null=False, blank=False
    )
    short_name = models.SlugField(
        db_column="short_name", max_length=255, null=False, blank=False
    )
    description = models.CharField(
        db_column="description", max_length=255, null=False, blank=False
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        db_table = "categories"


class Products(models.Model):
    barcode = models.CharField(
        db_column="barcode", max_length=25, unique=True, null=False, blank=False
    )
    name = models.CharField(
        db_column="name", max_length=255, unique=True, null=False, blank=False
    )
    short_name = models.SlugField(
        db_column="short_name", max_length=255, null=False, blank=False
    )
    category = models.ForeignKey(
        "Categories",
        db_column="category",
        on_delete=models.CASCADE,
        related_name="products_category",
    )
    if not settings.AWS:
        main_image = models.FileField(
            storage=FileSystemStorage(),
            upload_to=settings.AWS_PUBLIC_MEDIA_LOCATION + "/products/main/",
            db_column="main_image",
            null=True,
            blank=True,
        )
    else:
        main_image = models.FileField(
            storage=ProductMainPrictureStorage(),
            db_column="main_image",
            null=True,
            blank=True,
        )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        db_table = "products"


# class Document(models.Model):
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     upload = models.FileField()

#     class Meta:
#         verbose_name = "Document"
#         verbose_name_plural = "Documents"
#         db_table = "documents"


# class PrivateDocument(models.Model):
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     upload = models.FileField(storage=PrivateMediaStorage())
#     user = models.ForeignKey(Users, related_name='documents',on_delete=models.CASCADE)
#     meta_data = models.TextField(default="", null=True, blank=True)
