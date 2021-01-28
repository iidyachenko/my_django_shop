from django.core.management import call_command
from django.test import TestCase, Client

# Create your tests here.
from mainapp.models import ProductCategories, Product


class TestMainappSmoke(TestCase):

    def setUp(self):
        test_category = ProductCategories.objects.create(name='Test')
        Product.objects.create(category=test_category, name='Product Test1', short_desc='Product Test1')
        Product.objects.create(category=test_category, name='Product Test2', short_desc='Product Test2')
        Product.objects.create(category=test_category, name='Product Test3', short_desc='Product Test3')
        Product.objects.create(category=test_category, name='Product Test4', short_desc='Product Test4')

        self.client = Client()

    def test_mainapp_urls(self):

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

    def test_product_pages(self):

        count = 0
        for product in ProductCategories.objects.all():
            response = self.client.get(f'/products/{product.pk}/')
            self.assertEqual(response.status_code, 200)
            count += 1
        self.assertEqual(count, 1)

        count = 0
        for product in Product.objects.all():
            response = self.client.get(f'/products/product/{product.pk}/')
            self.assertEqual(response.status_code, 200)
            count += 1
        self.assertEqual(count, 4)

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')
