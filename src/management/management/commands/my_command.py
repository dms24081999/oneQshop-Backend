from django.core.management.base import BaseCommand, CommandError
import csv

# import any models, django modules, or packages here
from products_app.models import Products, Categories

"""
python manage.py my_command --files "/mnt/f/Projects/BE Project/main-backend/src/management/csv/images.csv"
"""


class Command(BaseCommand):
    help = "Carries out my custom admin function"

    def add_arguments(self, parser):
        parser.add_argument("--files", type=str, help="Categories CSV file path.")

    def handle(self, *args, **kwargs):
        # Users.objects.all().delete()
        files = csv.DictReader(open(kwargs["files"]))
        for row in files:
            print("Creating image:", row["barcode"])
            p, created = Products.objects.get_or_create(
                barcode=row["barcode"],
                name=row["name"],
                short_name=row["short_name"],
                category=Categories.objects.get(id=int(row["category"])),
            )
            if created:
                p.images.add(*row["images"].split())
                # p.images.remove(100)
                # p.images.set(obj)
