from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

# For listing all users and creating new user, to view a single user append '/1' that is '/id' in the URL  path 'list/fullinfo'
router.register(r"product", ProductsFullInfoAPIView) 
router.register(r"category", CategoriesFullInfoAPIView)

urlpatterns = [
    path("", include(router.urls)),
]

