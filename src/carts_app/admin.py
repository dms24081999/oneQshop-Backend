from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import Cart


@admin.register(Cart)
class CartsAdmin(ImportExportModelAdmin):
    pass
