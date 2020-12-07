import os
import json

from django.conf import settings
from django.shortcuts import render, get_object_or_404

# Create your views here.
from basketapp.models import Basket
from mainapp.models import Product, ProductCategories, Location

my_user = 'Игорь'


def main(request):
    products_list_db = Product.objects.filter(main_flag=True)

    content = {
        'title': 'Главная',
        'my_user': my_user,
        'products_list_db': products_list_db
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    category_list = ProductCategories.objects.all()

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    if pk is not None:
        if pk == 0:
            product_list = Product.objects.all()
            category = {'name': 'все', 'pk': 0}
        else:
            product_list = Product.objects.filter(category__pk=pk)
            category = get_object_or_404(ProductCategories.objects, pk=pk)

        content = {'title': 'Продукты',
                   'category_list': category_list,
                   'product_list': product_list,
                   'category': category,
                   'basket': basket}
        return render(request, 'mainapp/product_list.html', content)

    main_product = Product.objects.get(name='IPhone 12 Pro Max')
    content = {
        'title': 'Продукты',
        'my_user': my_user,
        'category_list': category_list,
        'main_product': main_product,
        'basket': basket,
    }
    return render(request, 'mainapp/products.html', content)


def contact(request):

    locations = Location.objects.all()

    content = {
        'title': 'Контакты',
        'my_user': my_user,
        'locations': locations
    }
    return render(request, 'mainapp/contact.html', content)
