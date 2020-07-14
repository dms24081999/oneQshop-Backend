from django.core.management.base import BaseCommand, CommandError
import csv
import os
from django.core.files import File


# import any models, django modules, or packages here
from django.contrib.auth import get_user_model

Users = get_user_model()
from products_app.models import ProductImages, Products, Categories

"""
python manage.py populate_db --users_file "/mnt/f/Projects/BE Project/main-backend/src/management/csv/users.csv" \
    --categories_file "/mnt/f/Projects/BE Project/main-backend/src/management/csv/categories.csv" \
        --product_images_file "/mnt/f/Projects/BE Project/main-backend/src/management/csv/product_images.csv" \
            --products_file "/mnt/f/Projects/BE Project/main-backend/src/management/csv/products.csv"
"""


class Command(BaseCommand):
    help = "Create random users"

    def add_arguments(self, parser):
        parser.add_argument("--users_file", type=str, help="Users CSV file path.")
        parser.add_argument(
            "--categories_file", type=str, help="Categories CSV file path."
        )
        parser.add_argument(
            "--product_images_file", type=str, help="Product Images CSV file path."
        )
        parser.add_argument("--products_file", type=str, help="Products CSV file path.")

    def handle(self, *args, **kwargs):
        # Delete all data
        print("Deleting Users Table")
        Users.objects.all().delete()
        print("Deleting Products Table")
        Products.objects.all().delete()
        print("Deleting ProductImages Table")
        ProductImages.objects.all().delete()
        print("Deleting Categories Table")
        Categories.objects.all().delete()

        # Admin
        print("Creating Admin")
        user, created = Users.objects.get_or_create(
            username="admin", email="dms24081999@gmail.com"
        )
        if created:
            user.set_password("24081999")
            user.staff = True
            user.admin = True
            user.save()

        # Users
        users = csv.DictReader(open(kwargs["users_file"]))
        for row in users:
            print("Creating User:", row["username"])
            user, created = Users.objects.get_or_create(
                username=row["username"], email=row["email"]
            )
            if created:
                user.set_password(row["password"])
                user.save()

        # Categories
        categories = csv.DictReader(open(kwargs["categories_file"]))
        for row in categories:
            print("Creating Category:", row["name"])
            user, created = Categories.objects.get_or_create(
                id=row["id"], name=row["name"], short_name=row["short_name"]
            )

        # Product Images
        product_images = csv.DictReader(open(kwargs["product_images_file"]))
        basepath = "/mnt/f/Projects/BE Project/GroceryStoreDataset"
        for row in product_images:
            print("Creating Product Image:", row["id"])
            f = File(open(os.path.join(basepath, row["image"]), "rb"))
            productimage, created = ProductImages.objects.get_or_create(
                id=row["id"], main_image=row["main_image"]
            )
            if created:
                productimage.image.save(os.path.split(f.name)[1], f)
                productimage.save()

        # Products
        products = csv.DictReader(open(kwargs["products_file"]))
        for row in products:
            print("Creating Product:", row["barcode"])
            product, created = Products.objects.get_or_create(
                barcode=row["barcode"],
                name=row["name"],
                short_name=row["short_name"],
                category=Categories.objects.get(id=int(row["category"])),
            )
            if created:
                product.images.add(
                    *row["images"].split()
                )  # p.images.remove(100) # p.images.set(obj)
