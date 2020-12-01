from django.shortcuts import render


# Create your views here.

links_menu = [
    {"href": "products_all", "name": "Все"},
    {"href": "products_home", "name": "Дом"},
    {"href": "products_modern", "name": "Модерн"},
    {"href": "products_office", "name": "Офис"},
    {"href": "products_classic", "name": "Класика"},
]

my_user = 'Игорь'


def main(request):
    content = {
        'title': 'Главная',
        'my_user': my_user
    }
    return render(request, 'mainapp/index.html', content)


def products(request):

    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
        'my_user': my_user
    }
    return render(request, 'mainapp/products.html', content)


def contact(request):
    content = {
        'title': 'Контакты',
        'my_user': my_user
    }
    return render(request, 'mainapp/contact.html', content)


def products_all(request):
    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
        'my_user': my_user
    }
    return render(request, 'mainapp/products.html', content)


def products_home(request):
    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
        'my_user': my_user
    }
    return render(request, 'mainapp/products.html', content)


def products_office(request):
    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
        'my_user': my_user
    }
    return render(request, 'mainapp/products.html', content)


def products_modern(request):
    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
        'my_user': my_user
    }
    return render(request, 'mainapp/products.html', content)


def products_classic(request):
    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
        'my_user': my_user
    }
    return render(request, 'mainapp/products.html', content)