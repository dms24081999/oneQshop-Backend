from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import *


@admin.register(Products)
class ProductsAdmin(ImportExportModelAdmin):
    pass


@admin.register(ProductImages)
class ProductImagesAdmin(ImportExportModelAdmin):
    pass


@admin.register(Categories)
class CategoriesAdmin(ImportExportModelAdmin):
    pass


@admin.register(Brands)
class BrandsAdmin(ImportExportModelAdmin):
    pass


@admin.register(Invoices)
class ProductsAdmin(ImportExportModelAdmin):
    pass


@admin.register(Carts)
class CartsAdmin(ImportExportModelAdmin):
    pass
