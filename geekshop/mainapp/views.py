import os
import json
import random

from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

# Create your views here.
from basketapp.models import Basket
from mainapp.models import Product, ProductCategories, Location

my_user = 'Игорь'
category_list = ProductCategories.objects.all()


def get_hot_product():
    products_all = Product.objects.all()
    return random.choice(list(products_all))


def get_same_products(hot_product):
    return Product.objects.filter(category__pk=hot_product.category.pk).exclude(pk=hot_product.pk)


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return []


def main(request):
    products_list_db = Product.objects.filter(main_flag=True)

    content = {
        'title': 'Главная',
        'my_user': my_user,
        'products_list_db': products_list_db,
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None, page=1):

    if pk is not None:
        if pk == 0:
            product_list = Product.objects.all()
            category = {'name': 'все', 'pk': 0}
        else:
            product_list = Product.objects.filter(category__pk=pk)
            category = get_object_or_404(ProductCategories.objects, pk=pk)

        paginator = Paginator(product_list, 2)
        try:
            product_paginator = paginator.page(page)
        except PageNotAnInteger:
            product_paginator = paginator.page(1)
        except EmptyPage:
            product_paginator = paginator.page(paginator.num_pages)

        content = {'title': 'Продукты',
                   'category_list': category_list,
                   'product_list': product_paginator,
                   'category': category,
                   'basket': get_basket(request.user),
                   'hot_product': get_hot_product(),
                   }
        return render(request, 'mainapp/product_list.html', content)

    main_product = get_hot_product()
    content = {
        'title': 'Продукты',
        'my_user': my_user,
        'category_list': category_list,
        'main_product': main_product,
        'basket': get_basket(request.user),
        'same_products': get_same_products(main_product)
    }
    return render(request, 'mainapp/products.html', content)


def product(request, pk):

    _product = get_object_or_404(Product, pk=pk)

    content = {
        'title': _product.name,
        'category_list': category_list,
        'product': _product,
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/product.html', content)

def contact(request):

    locations = Location.objects.all()

    content = {
        'title': 'Контакты',
        'my_user': my_user,
        'locations': locations,
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/contact.html', content)
