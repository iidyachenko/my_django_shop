import os
import json
import random

from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string

from basketapp.models import Basket
from mainapp.models import Product, ProductCategories, Location

my_user = 'Игорь'


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategories.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategories.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategories, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategories, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_main_products():
    if settings.LOW_CACHE:
        key = 'main_products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True, main_flag=True).select_related(
                'category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def get_hot_product():
    products_all = get_products()
    return random.choice(list(products_all))


def get_same_products(hot_product):
    return Product.objects.filter(category__pk=hot_product.category.pk).exclude(pk=hot_product.pk)


def main(request):
    products_list_db = get_main_products()

    content = {
        'title': 'Главная',
        'my_user': my_user,
        'products_list_db': products_list_db,
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None, page=1):
    category_list = get_links_menu()
    if pk is not None:
        if pk == 0:
            product_list = get_products()
            category = {'name': 'все', 'pk': 0}
        else:
            product_list = get_products_in_category_orederd_by_price(pk)
            category = get_category(pk)

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
                   'hot_product': get_hot_product(),
                   }
        return render(request, 'mainapp/product_list.html', content)


def product(request, pk):
    category_list = get_links_menu()

    _product = get_product(pk)

    content = {
        'title': _product.name,
        'category_list': category_list,
        'product': _product,
    }
    return render(request, 'mainapp/product.html', content)


def contact(request):
    locations = Location.objects.all()

    content = {
        'title': 'Контакты',
        'my_user': my_user,
        'locations': locations,
    }
    return render(request, 'mainapp/contact.html', content)


def products_ajax(request, pk=None, page=1):
    if request.is_ajax():

        category_list = get_links_menu()
        if pk is not None:
            if pk == 0:
                product_list = get_products()
                category = {'name': 'все', 'pk': 0}
            else:
                product_list = get_products_in_category_orederd_by_price(pk)
                category = get_category(pk)

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
                       'hot_product': get_hot_product(),
                       }
            result = render_to_string(
                'mainapp/includes/inc_products_list_content.html',
                context=content,
                request=request)
            return JsonResponse({'result': result})

        main_product = get_hot_product()
        content = {
            'title': 'Продукты',
            'my_user': my_user,
            'category_list': category_list,
            'main_product': main_product,
            'same_products': get_same_products(main_product)
        }

        result = render_to_string(
            'mainapp/includes/inc_products_list_content.html',
            context=content,
            request=request)

        return JsonResponse({'result': result})
