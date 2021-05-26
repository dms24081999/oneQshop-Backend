from django.http import response
from django.test import TestCase, Client
from django.urls import reverse
from django.urls.base import resolve
from products_app.models import ProductImages, Products, Categories, Brands, Carts
from django.contrib.auth import get_user_model

Users = get_user_model()


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_cart = reverse("cart_info-list")
        self.login_url = reverse("knox_login")

        user, created = Users.objects.get_or_create(
            username="dms24081999", email="dms24081999@gmail.com"
        )
        if created:
            user.set_password("Delta24@doms")
            user.save()
        category, created = Categories.objects.get_or_create(
            name="Shoes", short_name="shoes"
        )
        brand, created = Brands.objects.get_or_create(
            name="Rebook", short_name="Rebook"
        )
        product, created = Products.objects.get_or_create(
            barcode="100",
            name="100",
            short_name="100",
            brand=Brands.objects.get(id=int(brand.id)),
            price=5.0,
            count=15,
        )
        if created:
            product.categories.add(*[category.id])

    def test_db(self):
        self.assertEquals(Categories.objects.all().count(), 1)
        self.assertEquals(Brands.objects.all().count(), 1)
        self.assertEquals(Products.objects.all().count(), 1)

    def test_add_to_cart_1(self):
        response = self.client.post(
            self.login_url,
            data={"username": "dms24081999@gmail.com", "password": "Delta24@doms"},
        )
        header = {"HTTP_AUTHORIZATION": "Token " + response.json()["token"]}
        response = self.client.post(
            self.create_cart,
            data={
                "user_id": Users.objects.all()[0].id,
                "product_id": Products.objects.all()[0].id,
                "count": 5,
            },
            **header
        )
        self.assertEquals(response.json()["count"], 5)
        self.assertEquals(response.json()["cart_details"]["count"], 10)
        response = self.client.post(
            self.create_cart,
            data={
                "user_id": Users.objects.all()[0].id,
                "product_id": Products.objects.all()[0].id,
                "count": 15,
            },
            **header
        )
        self.assertEquals(response.json()["count"], 15)
        self.assertEquals(response.json()["cart_details"]["count"], 0)
        response = self.client.post(
            self.create_cart,
            data={
                "user_id": Users.objects.all()[0].id,
                "product_id": Products.objects.all()[0].id,
                "count": 16,
            },
            **header
        )
        self.assertEquals(response.json()["count"], 15)
        self.assertEquals(response.json()["cart_details"]["count"], 0)
