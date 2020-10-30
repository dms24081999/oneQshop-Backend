from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

# For listing all users and creating new user, to view a single user append '/1' that is '/id' in the URL  path 'list/fullinfo'
router.register(r"product", ProductsFullInfoAPIView)
router.register(r"image", ProductImagesFullInfoAPIView)
router.register(r"category", CategoriesFullInfoAPIView)
# ImagesTrainingAPI
urlpatterns = [
    path("", include(router.urls)),
    path("dataset/images/", ProductImagesTrainingAPI.as_view()),
    path("dataset/names/", ProductNamesTrainingAPI.as_view()),
    path(
        "recommend/visual/<int:pk>/", ProductVisualSimilarityRecommendationAPI.as_view()
    ),
    path("recommend/name/<int:pk>/", ProductNameSimilarityRecommendationAPI.as_view()),
    path("recommend/user/", UserBasedCollaborativeFilteringRecommendationAPI.as_view()),
    path("uploadtest/", MyUploadView.as_view()),
]
