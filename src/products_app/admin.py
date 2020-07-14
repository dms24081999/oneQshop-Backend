from django.contrib import admin

# Register your models here.
from .models import Products, ProductImages, Categories

admin.site.register(Products)
admin.site.register(ProductImages)
admin.site.register(Categories)
