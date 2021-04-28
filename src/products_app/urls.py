from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

# For listing all users and creating new user, to view a single user append '/1' that is '/id' in the URL  path 'list/fullinfo'
router.register(r"product", ProductsFullInfoAPIView)
router.register(r"image", ProductImagesFullInfoAPIView)
router.register(r"category", CategoriesFullInfoAPIView)
router.register(r"cart", CartsFullInfoAPIView)

# ImagesTrainingAPI
urlpatterns = [
    path("dataset/images/", ProductImagesTrainingAPI.as_view()),
    path("dataset/names/", ProductNamesTrainingAPI.as_view()),
    path("barcodes/", ProductBarCodesAPI.as_view()),
    path(
        "recommend/visual/<int:pk>/", ProductVisualSimilarityRecommendationAPI.as_view()
    ),
    path("recommend/name/<int:pk>/", ProductNameSimilarityRecommendationAPI.as_view()),
    path("recommend/user/", UserBasedCollaborativeFilteringRecommendationAPI.as_view()),
    path(
        "recommend/item/<int:pk>/",
        ItemBasedCollaborativeFilteringRecommendationAPI.as_view(),
    ),
    path("uploadtest/", MyUploadView.as_view()),
    path("count/cart/", GetCartCountAPI.as_view()),
    path("", include(router.urls)),
]
