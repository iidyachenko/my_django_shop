import os
import json

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import BaseCommand

from authapp.models import ShopUser
from mainapp.models import Product, ProductCategories, Location

JSON_PATH = os.path.join(settings.BASE_DIR, 'mainapp/json')


def load_json_data(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), encoding='UTF-8') as json_file:
        return json.load(json_file)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_json_data("ProductCategories")
        ProductCategories.objects.all().delete()
        for category in categories:
            ProductCategories.objects.create(**category)

        products = load_json_data("Product")
        Product.objects.all().delete()
        for product in products:
            category_name = product['category']
            product['category'] = ProductCategories.objects.get(name=category_name)
            Product.objects.create(**product)

        locations = load_json_data("contacts")
        Location.objects.all().delete()
        for location in locations:
            Location.objects.create(**location)

        ShopUser.objects.create_superuser('django', "django@gb.ru", 'geekbrains', age=30)
