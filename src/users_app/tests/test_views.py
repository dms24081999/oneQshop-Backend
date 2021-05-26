from django.http import response
from django.test import TestCase, Client
from django.urls import reverse
from django.urls.base import resolve
from django.contrib.auth import get_user_model

Users = get_user_model()


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("create-user")
        self.login_url = reverse("knox_login")
        self.logout_url = reverse("knox_logout")
        self.logout_all_url = reverse("knox_logoutall")
        self.reset_password_request_url = reverse("reset-password-request")
        self.reset_password_confirm_url = reverse("reset-password-confirm")
        self.change_password_url = reverse("change-password")
        self.user_info_list = reverse("user_info-list")
        self.create_user = self.client.post(
            self.register_url,
            data={
                "username": "dms24081999",
                "first_name": "Dominic",
                "last_name": "Silveira",
                "email": "dms24081999@gmail.com",
                "password": "Delta@24d",
                "phone_number": "+919594183245",
            },
        )

    def test_register_POST(self):
        self.assertEquals(self.create_user.status_code, 201)

    def test_login_POST(self):
        response = self.client.post(
            self.login_url,
            data={"username": "dms24081999@gmail.com", "password": "Delta@24d"},
        )
        self.assertEquals(response.status_code, 200)

    def test_logout_POST(self):
        header = {"HTTP_AUTHORIZATION": "Token " + self.create_user.json()["token"]}
        response = self.client.post(self.logout_url, data={}, **header)
        self.assertEquals(response.status_code, 204)

    def test_logout_all_POST(self):
        header = {"HTTP_AUTHORIZATION": "Token " + self.create_user.json()["token"]}
        response = self.client.post(self.logout_all_url, data={}, **header)
        self.assertEquals(response.status_code, 204)

    def test_reset_password_request_POST(self):
        request_response = self.client.post(
            self.reset_password_request_url, data={"email": "dms24081999@gmail.com"}
        )
        self.assertEquals(request_response.status_code, 200)
        response = self.client.post(
            self.reset_password_confirm_url,
            data={
                "token": request_response.json()["token"],
                "password": "Delta@24doms",
            },
        )
        self.assertEquals(response.status_code, 200)
        response = self.client.post(
            self.login_url,
            data={"username": "dms24081999@gmail.com", "password": "Delta@24doms"},
        )
        self.assertEquals(response.status_code, 200)

    def test_change_password_request_POST(self):
        header = {"HTTP_AUTHORIZATION": "Token " + self.create_user.json()["token"]}
        response = self.client.put(
            self.change_password_url,
            data={"old_password": "Delta@24d", "new_password": "Delta@24doms"},
            content_type="application/json",
            **header
        )
        self.assertEquals(response.status_code, 200)
        response = self.client.post(
            self.login_url,
            data={"username": "dms24081999@gmail.com", "password": "Delta@24doms"},
        )
        self.assertEquals(response.status_code, 200)

    def test_user_info_list_request_POST(self):
        header = {"HTTP_AUTHORIZATION": "Token " + self.create_user.json()["token"]}
        response = self.client.get(self.user_info_list, **header)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Users.objects.all().count(), 1)
        self.assertEquals(response.json()[0]["email"], "dms24081999@gmail.com")
