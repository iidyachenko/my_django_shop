from django.db import models

# Create your models here.


class ProductCategories(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="Имя")
    description = models.TextField(verbose_name="Описание")
    is_active = models.BooleanField(default=True, verbose_name='активно')

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategories, on_delete=models.CASCADE, verbose_name="Категория")
    name = models.CharField(max_length=120, unique=True, verbose_name="Названиие")
    image = models.ImageField(upload_to="products_images", blank=True, verbose_name="Изображение")
    short_desc = models.CharField(max_length=120, unique=True, verbose_name="Названиие")
    description = models.TextField(verbose_name="Описание", blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="Цена")
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name="Количество на складе")
    main_flag = models.BooleanField(default=False, verbose_name="Наличие на главной")
    is_active = models.BooleanField(default=True, verbose_name='активно')

    def __str__(self):
        return f"{self.name}  {self.category.name}"

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by('category', 'name')


class Location(models.Model):
    city = models.CharField(max_length=120, unique=True, verbose_name="Город")
    phone = models.CharField(max_length=20,  verbose_name="Телефон")
    email = models.CharField(max_length=60, unique=True, verbose_name="Email")
    address = models.TextField(verbose_name="Адрес", blank=True)
    map_code = models.TextField(verbose_name="Код для карты", blank=True)

    def __str__(self):
        return f"{self.city}"
    