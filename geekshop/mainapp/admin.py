from django.contrib import admin

# Register your models here.
from mainapp.models import ProductCategories, Product, Location

admin.site.register(ProductCategories)
admin.site.register(Product)
admin.site.register(Location)