from django.conf import settings
from django.core.management import call_command
from django.test import TestCase, Client

# Create your tests here.
from authapp.models import ShopUser
from mainapp.models import ProductCategories, Product


class TestUserAuth(TestCase):

    def setUp(self):
        test_category = ProductCategories.objects.create(name='Test')
        Product.objects.create(category=test_category, name='Product Test1', short_desc='Product Test1')
        Product.objects.create(category=test_category, name='Product Test2', short_desc='Product Test2')
        Product.objects.create(category=test_category, name='Product Test3', short_desc='Product Test3')
        Product.objects.create(category=test_category, name='Product Test4', short_desc='Product Test4')

        self.client = Client()

        self.superuser = ShopUser.objects.create_superuser('django', 'django2@geekshop.local', 'geekbrains')

        self.user = ShopUser.objects.create_user('test_user', 'test_user@geekshop.local', 'geekbrains')

        self.user_with__first_name = ShopUser.objects.create_user('igor', 'igor@geekshop.local', 'geekbrains',
                                                                  first_name='Игорь')

    def test_user_login(self):

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['title'], 'Главная')
        self.assertNotContains(response, 'Пользователь', status_code=200)

        self.client.login(username='django', password='geekbrains')
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.superuser)

        response = self.client.get('/')
        self.assertContains(response, 'Пользователь', status_code=200)
        self.assertEqual(response.context['user'], self.superuser)

    def test_user_logout(self):
        self.client.login(username='django', password='geekbrains')
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.superuser)

        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

    def test_redirect(self):
        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/auth/login/?next=/basket/')

        self.client.login(username='django', password='geekbrains')
        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/basket/')

    def test_user_register(self):
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], 'Регистрация')
        self.assertTrue(response.context['user'].is_anonymous)

        new_user_data = {
            'username': 'test2',
            'first_name': 'test',
            'last_name': 'test',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'test2@geekshop.local',
            'age': '22'}

        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, 302)

        new_user = ShopUser.objects.get(username=new_user_data['username'])
        self.assertEqual(new_user.username, 'test2')
        activation_url = f"{settings.DOMAIN_NAME}/auth/verify/{new_user_data['email']}/{new_user.activation_key}"

        # self.assertEqual(activation_url,'http://localhost:8000/auth/verify/django_file_test@mail.local/82e0f6e5d9781e3553221804774ecbe95758155b')
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 200)

    def test_user_wrong_register(self):
        new_user_data = {
            'username': 'teen',
            'first_name': 'Мэри',
            'last_name': 'Поппинс',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'merypoppins@geekshop.local',
            'age': '17'}

        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'register_form', 'age', 'Вам меньше 18 лет')

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')