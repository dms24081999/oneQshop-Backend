from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import Products, ProductImages, Categories, Document


@admin.register(Products)
class ProductsAdmin(ImportExportModelAdmin):
    pass


@admin.register(ProductImages)
class ProductImagesAdmin(ImportExportModelAdmin):
    pass


@admin.register(Categories)
class CategoriesAdmin(ImportExportModelAdmin):
    pass


@admin.register(Document)
class ProductsAdmin(ImportExportModelAdmin):
    pass
