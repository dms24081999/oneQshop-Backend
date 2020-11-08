from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

# For listing all users and creating new user, to view a single user append '/1' that is '/id' in the URL  path 'list/fullinfo'
router.register(r"", UsersFullInfoAPIView)

urlpatterns = [
    path("login/", LoginView.as_view(), name="knox_login"),
    path("logout/", LogoutView.as_view(), name="knox_logout"),
    path("logoutall/", LogoutAllView.as_view(), name="knox_logoutall"),
    path(
        "reset-password/validate_token/",
        ResetPasswordValidateToken.as_view(),
        name="reset-password-validate",
    ),
    path(
        "reset-password/confirm/",
        ResetPasswordConfirm.as_view(),
        name="reset-password-confirm",
    ),
    path(
        "reset-password/",
        ResetPasswordRequestToken.as_view(),
        name="reset-password-request",
    ),
    path("create/", UsersCreateInfoAPIView.as_view()),
    path("is-authenticated/", UsersIsAuthenticatedAPIView.as_view()),
    path("change-password/", ChangePasswordAPIView.as_view()),
    path("", include(router.urls)),
    # path("user/currentuser/", CurrentUserAPIView.as_view()),
]
