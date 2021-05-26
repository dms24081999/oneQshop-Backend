from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

# For listing all users and creating new user, to view a single user append '/1' that is '/id' in the URL  path 'list/fullinfo'
router.register(r"product", ProductsFullInfoAPIView, basename="product_info")
router.register(r"image", ProductImagesFullInfoAPIView, basename="image_info")
router.register(r"category", CategoriesFullInfoAPIView, basename="category_info")
router.register(r"cart", CartsFullInfoAPIView, basename="cart_info")
router.register(r"invoice", InvoicesFullInfoAPIView, basename="invoice_info")

# ImagesTrainingAPI
urlpatterns = [
    path(
        "dataset/images/",
        ProductImagesTrainingAPI.as_view(),
        name="product_images_training",
    ),
    path(
        "dataset/names/",
        ProductNamesTrainingAPI.as_view(),
        name="product_names_training",
    ),
    path("barcodes/", ProductBarCodesAPI.as_view(), name="product_barcodes"),
    path(
        "recommend/visual/<int:pk>/",
        ProductVisualSimilarityRecommendationAPI.as_view(),
        name="product_visual_recommend",
    ),
    path(
        "recommend/name/<int:pk>/",
        ProductNameSimilarityRecommendationAPI.as_view(),
        name="product_name_recommend",
    ),
    path("recommend/user/", UserBasedCollaborativeFilteringRecommendationAPI.as_view()),
    path(
        "recommend/item/<int:pk>/",
        ItemBasedCollaborativeFilteringRecommendationAPI.as_view(),
    ),
    # path("uploadtest/", MyUploadView.as_view()),
    path("count/cart/", GetCartCountAPI.as_view(), name="cart_count"),
    path("paid/cart/", CartsPaidAPIView.as_view(), name="cart_paid"),
    path("", include(router.urls)),
]
