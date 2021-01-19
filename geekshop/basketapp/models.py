from django.conf import settings
from django.db import models

# Create your models here.
from django.utils.functional import cached_property

from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="basket")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(auto_now_add=True, verbose_name='время')

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        __total_items = self.get_items_cached
        __total_quantity = sum(list(map(lambda x: x.quantity, __total_items)))
        return __total_quantity

    @property
    def total_cost(self):
        __total_items = self.get_items_cached
        __total_cost = sum(list(map(lambda x: x.product_cost, __total_items)))
        return __total_cost

    @staticmethod
    def get_items(user):
        return Basket.objects.filter(user=user).order_by('product__category')

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)
