from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to="user_avatars", blank=True, verbose_name="аватар")
    age = models.SmallIntegerField(verbose_name="возраст")
