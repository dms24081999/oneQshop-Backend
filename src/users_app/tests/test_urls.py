from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users_app.views import (
    LoginView,
    LogoutView,
    LogoutAllView,
    ResetPasswordValidateToken,
    ResetPasswordConfirm,
    ResetPasswordRequestToken,
    UsersCreateInfoAPIView,
    UsersIsAuthenticatedAPIView,
    ChangePasswordAPIView,
)


class TestUrls(SimpleTestCase):
    def test_login_url_is_resolved(self):
        url = reverse("knox_login")
        self.assertEquals(resolve(url).func.view_class, LoginView)

    def test_logout_url_is_resolved(self):
        url = reverse("knox_logout")
        self.assertEquals(resolve(url).func.view_class, LogoutView)

    def test_logout_all_url_is_resolved(self):
        url = reverse("knox_logoutall")
        self.assertEquals(resolve(url).func.view_class, LogoutAllView)

    def test_reset_password_validate_url_is_resolved(self):
        url = reverse("reset-password-validate")
        self.assertEquals(resolve(url).func.view_class, ResetPasswordValidateToken)

    def test_reset_password_confirm_url_is_resolved(self):
        url = reverse("reset-password-confirm")
        self.assertEquals(resolve(url).func.view_class, ResetPasswordConfirm)

    def test_reset_password_request_url_is_resolved(self):
        url = reverse("reset-password-request")
        self.assertEquals(resolve(url).func.view_class, ResetPasswordRequestToken)

    def test_create_user_url_is_resolved(self):
        url = reverse("create-user")
        self.assertEquals(resolve(url).func.view_class, UsersCreateInfoAPIView)

    def test_is_authenticated_url_is_resolved(self):
        url = reverse("is-authenticated")
        self.assertEquals(resolve(url).func.view_class, UsersIsAuthenticatedAPIView)

    def test_change_password_url_is_resolved(self):
        url = reverse("change-password")
        self.assertEquals(resolve(url).func.view_class, ChangePasswordAPIView)
