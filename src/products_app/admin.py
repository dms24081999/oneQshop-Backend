from django.contrib import admin

# Register your models here.
from .models import Document, PrivateDocument

admin.site.register(Document)
admin.site.register(PrivateDocument)