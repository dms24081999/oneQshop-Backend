from django.contrib import admin

# Register your models here.
from .models import Products, ProductImages

admin.site.register(Products)
admin.site.register(ProductImages)
