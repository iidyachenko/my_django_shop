import os
import json

from django.conf import settings
from django.shortcuts import render


# Create your views here.
from mainapp.models import Product, ProductCategories

my_user = 'Игорь'


def main(request):
    products_list_db = Product.objects.exclude(image__exact='')

    content = {
        'title': 'Главная',
        'my_user': my_user,
        'products_list_db': products_list_db
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    category_list = ProductCategories.objects.all()
    main_product = Product.objects.get(name='IPhone 12 Pro Max')
    content = {
        'title': 'Продукты',
        'my_user': my_user,
        'category_list': category_list,
        'main_product': main_product
    }
    return render(request, 'mainapp/products.html', content)


def contact(request):

    file_path = os.path.join(settings.BASE_DIR, 'contacts.json')
    with open(file_path, encoding='utf8') as file_contacts:
        locations = json.load(file_contacts)

    content = {
        'title': 'Контакты',
        'my_user': my_user,
        'locations': locations
    }
    return render(request, 'mainapp/contact.html', content)
