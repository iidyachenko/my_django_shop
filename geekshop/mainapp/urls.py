from django.conf import settings
from django.conf.urls import static
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.products, name='index'),
    path('<int:pk>/', cache_page(3600)(mainapp.products), name='category'),
    path('<int:pk>/<int:page>/', mainapp.products, name='page'),
    path('product/<int:pk>/', mainapp.product, name='product')
]