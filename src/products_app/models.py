from django.db import models
from django.conf import settings

from mainsite.storage_backends import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model

Users = get_user_model()


class Brands(models.Model):
    name = models.CharField(
        db_column="name", max_length=255, unique=True, null=False, blank=False
    )
    short_name = models.SlugField(
        db_column="short_name", max_length=255, null=False, blank=False
    )
    description = models.CharField(
        db_column="description", max_length=255, null=True, blank=True
    )
    is_deleted = models.BooleanField(default=False, db_column="is_deleted")

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        db_table = "brands"

    def __str__(self):
        return "(" + str(self.pk) + ") " + self.name


class Categories(models.Model):
    name = models.CharField(
        db_column="name", max_length=255, unique=True, null=False, blank=False
    )
    short_name = models.SlugField(
        db_column="short_name", max_length=255, null=False, blank=False
    )
    description = models.CharField(
        db_column="description", max_length=255, null=True, blank=True
    )
    if not settings.AWS:
        image = models.FileField(
            storage=FileSystemStorage(),
            upload_to=settings.AWS_PUBLIC_MEDIA_LOCATION + "/categories/",
            db_column="image",
            null=True,
            blank=True,
        )
    else:
        image = models.FileField(
            storage=CategoryPictureStorage(), db_column="image", null=True, blank=True
        )
    is_deleted = models.BooleanField(default=False, db_column="is_deleted")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        db_table = "categories"

    def __str__(self):
        return "(" + str(self.pk) + ") " + self.name


class ProductImages(models.Model):
    if not settings.AWS:
        image = models.FileField(
            storage=FileSystemStorage(),
            upload_to=settings.AWS_PUBLIC_MEDIA_LOCATION + "/products/main/",
            db_column="image",
            null=True,
            blank=True,
        )
    else:
        image = models.FileField(
            storage=ProductMainPictureStorage(),
            db_column="image",
            null=True,
            blank=True,
        )
    main_image = models.BooleanField(default=False, db_column="main_image")
    is_deleted = models.BooleanField(default=False, db_column="is_deleted")

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        db_table = "product_images"

    def __str__(self):
        return "(" + str(self.pk) + ") " + self.image.name


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
    categories = models.ManyToManyField(
        Categories,
        related_name="product_categories",
        blank=True,
        db_column="categories",
    )
    brand = models.ForeignKey(
        Brands,
        db_column="brand",
        on_delete=models.PROTECT,
        related_name="product_brand",
        blank=True,
        null=True,
    )
    images = models.ManyToManyField(
        ProductImages, related_name="product_images", blank=True, db_column="images"
    )
    price = models.FloatField(null=False, blank=False, default=5.0, db_column="price")
    count = models.IntegerField(null=False, blank=False, default=15, db_column="count")
    is_deleted = models.BooleanField(default=False, db_column="is_deleted")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        db_table = "products"

    def __str__(self):
        return "(" + str(self.pk) + ") " + self.name


class Carts(models.Model):
    cart_history_id = models.IntegerField(default=0, db_column="cart_history_id")
    user_id = models.ForeignKey(
        Users,
        db_column="user_id",
        on_delete=models.PROTECT,
        related_name="cart_user_id",
    )
    product_id = models.ForeignKey(
        Products,
        db_column="product_id",
        on_delete=models.PROTECT,
        related_name="cart_product_id",
    )
    count = models.IntegerField(default=0, db_column="count")
    ratings = models.IntegerField(default=5, db_column="ratings")
    is_deleted = models.BooleanField(default=False, db_column="is_deleted")

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        db_table = "carts"

    def __str__(self):
        return str(self.user_id) + " | " + str(self.product_id)


class Invoices(models.Model):
    if not settings.AWS:
        pdf_file = models.FileField(
            storage=FileSystemStorage(),
            upload_to=settings.AWS_PUBLIC_MEDIA_LOCATION + "/invoice/",
            db_column="pdf_file",
            null=True,
            blank=True,
        )
    else:
        pdf_file = models.FileField(
            storage=ProductMainPictureStorage(),
            db_column="pdf_file",
            null=True,
            blank=True,
        )
    user_id = models.ForeignKey(
        Users,
        db_column="user_id",
        on_delete=models.PROTECT,
        related_name="invoice_user_id",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, db_column="uploaded_at")
    is_deleted = models.BooleanField(default=False, db_column="is_deleted")

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"
        db_table = "invoices"

    def __str__(self):
        return "(" + str(self.pk) + ") " + self.pdf_file.name


# class Document(models.Model):
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     upload = models.FileField()
#     is_deleted = models.BooleanField(default=False)
#     class Meta:
#         verbose_name = "Document"
#         verbose_name_plural = "Documents"
#         db_table = "documents"

# class PrivateDocument(models.Model):
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     upload = models.FileField(storage=PrivateMediaStorage())
#     user = models.ForeignKey(Users, related_name='documents',on_delete=models.CASCADE)
#     meta_data = models.TextField(default="", null=True, blank=True)
