from django.test import TestCase
from mainapp.models import Product, ProductCategories


class ProductsTestCase(TestCase):
    def setUp(self):
        category = ProductCategories.objects.create(name="Телефоны")
        self.product_1 = Product.objects.create(name="Телефон1",
                                                category=category,
                                                short_desc="Телефон1",
                                                price=19990.5,
                                                quantity=150)

        self.product_2 = Product.objects.create(name="Телефон2",
                                                category=category,
                                                short_desc="Телефон2",
                                                price=29980.1,
                                                quantity=125,
                                                is_active=False)

        self.product_3 = Product.objects.create(name="Телефон3",
                                                category=category,
                                                short_desc="Телефон3",
                                                price=9980.1,
                                                quantity=115)

    def test_product_get(self):
        product_1 = Product.objects.get(name="Телефон1")
        product_2 = Product.objects.get(name="Телефон2")
        self.assertEqual(product_1, self.product_1)
        self.assertEqual(product_2, self.product_2)

    def test_product_print(self):
        product_1 = Product.objects.get(name="Телефон1")
        product_2 = Product.objects.get(name="Телефон2")
        self.assertEqual(str(product_1), 'Телефон1  Телефоны')
        self.assertEqual(str(product_2), 'Телефон2  Телефоны')

    def test_product_get_items(self):
        product_1 = Product.objects.get(name="Телефон1")
        product_3 = Product.objects.get(name="Телефон3")
        products = product_1.get_items()

        self.assertEqual(list(products), [product_1, product_3])
