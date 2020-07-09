from django.db import models
from django.conf import settings

from mainsite.storage_backends import PrivateMediaStorage

from django.contrib.auth import get_user_model
Users=get_user_model() 

class Document(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField()

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        db_table = "documents"


class PrivateDocument(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField(storage=PrivateMediaStorage())
    user = models.ForeignKey(Users, related_name='documents',on_delete=models.CASCADE)
    meta_data = models.TextField(default="", null=True, blank=True)
