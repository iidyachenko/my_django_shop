from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='media_folder_product')
def media_folder_product(string):
    if not string:
        string = 'products_images/default.jpg'

    return f'{settings.MEDIA_URL}{string}'


def media_folder_user(string):
    if not string:
        string = 'user_avatars/default.jpg'

    return f'{settings.MEDIA_URL}{string}'


register.filter('media_folder_user', media_folder_user)