from django.contrib import admin

# Register your models here.


from .forms import *
from .models import Addresses
from django.contrib.auth import get_user_model

Users = get_user_model()

admin.site.register(Users)
admin.site.register(Addresses)
