from django.core.management.base import BaseCommand, CommandError
import csv
import os
from django.core.files import File


# import any models, django modules, or packages here
from django.contrib.auth import get_user_model

Users = get_user_model()
from products_app.models import ProductImages, Products, Categories, Brands, Carts
from django.db import connection

"""
python manage.py populate_db --users_file "/mnt/f/Projects/BE Project/main-backend/src/management/csv/users.csv" \
    --categories_file "/mnt/f/Projects/BE Project/main-backend/src/management/csv/categories.csv" \
        --product_images_file "/mnt/f/Projects/BE Project/main-backend/src/management/csv/product_images.csv" \
            --products_file "/mnt/f/Projects/BE Project/main-backend/src/management/csv/products.csv"
"""


class Command(BaseCommand):
    help = "Populate db"

    def add_arguments(self, parser):
        parser.add_argument("--users_file", type=str, help="Users CSV file path.")
        parser.add_argument(
            "--categories_file", type=str, help="Categories CSV file path."
        )
        parser.add_argument("--brands_file", type=str, help="Brands CSV file path.")
        parser.add_argument(
            "--product_images_file", type=str, help="Product Images CSV file path."
        )
        parser.add_argument("--products_file", type=str, help="Products CSV file path.")
        parser.add_argument("--images_path", type=str, help="Product image files path.")

    def handle(self, *args, **kwargs):
        basepath = kwargs["images_path"]

        # Delete all data
        print("Deleting Users Table")
        Users.objects.all().delete()
        print("Deleting Products Table")
        Products.objects.all().delete()
        print("Deleting ProductImages Table")
        ProductImages.objects.all().delete()
        print("Deleting Categories Table")
        Categories.objects.all().delete()
        print("Deleting Brands Table")
        Brands.objects.all().delete()

        # delete sqlite sequence count
        # cursor = connection.cursor()
        # cursor.execute(
        #     "delete from sqlite_sequence where name='{}'".format(
        #         Users.objects.model._meta.db_table
        #     )
        # )
        # cursor.execute(
        #     "delete from sqlite_sequence where name='{}'".format(
        #         Products.objects.model._meta.db_table
        #     )
        # )
        # cursor.execute(
        #     "delete from sqlite_sequence where name='{}'".format(
        #         ProductImages.objects.model._meta.db_table
        #     )
        # )
        # cursor.execute(
        #     "delete from sqlite_sequence where name='{}'".format(
        #         Categories.objects.model._meta.db_table
        #     )
        # )
        # cursor.execute(
        #     "delete from sqlite_sequence where name='{}'".format(
        #         Brands.objects.model._meta.db_table
        #     )
        # )
        # cursor.execute(
        #     "delete from sqlite_sequence where name='{}'".format("products_images")
        # )
        # cursor.execute(
        #     "delete from sqlite_sequence where name='{}'".format("products_categories")
        # )
        # cursor.execute(
        #     "delete from sqlite_sequence where name='{}'".format(
        #         Carts.objects.model._meta.db_table
        #     )
        # )

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
            f = File(open(os.path.join(basepath, row["image"]), "rb"))
            category, created = Categories.objects.get_or_create(
                id=row["id"], name=row["name"], short_name=row["short_name"]
            )
            if created:
                category.image.save(os.path.split(f.name)[1], f)
                category.save()

        # Brands
        brands = csv.DictReader(open(kwargs["brands_file"]))
        for row in brands:
            print("Creating Brand:", row["name"])
            brand, created = Brands.objects.get_or_create(
                id=row["id"], name=row["name"], short_name=row["short_name"]
            )

        # Product Images
        product_images = csv.DictReader(open(kwargs["product_images_file"]))
        print(basepath)
        for row in product_images:
            print("Creating Product Image:", row["id"], row["image"])
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
            print("Creating Product:", row["barcode"], row["name"])
            product, created = Products.objects.get_or_create(
                barcode=row["barcode"],
                name=row["name"],
                short_name=row["short_name"],
                brand=Brands.objects.get(id=int(row["brand"])),
                price=5.0,
                count=15,
            )
            if created:
                # images: 1,2 in csv
                product.images.add(
                    *[int(id) for id in row["images"].split(",")]
                )  # p.images.remove(100) # p.images.set(obj)
                # categories: 1,2 in csv
                product.categories.add(
                    *[int(id) for id in row["categories"].split(",")]
                )
