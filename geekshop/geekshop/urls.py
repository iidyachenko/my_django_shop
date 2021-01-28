"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import static
from django.contrib import admin
from django.urls import path, include, re_path

import mainapp.views as mainapp

urlpatterns = [
    path('', mainapp.main, name='main'),
    path('products/', include('mainapp.urls', namespace='mainapp')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('order/', include('ordersapp.urls', namespace='order')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('contact/', mainapp.contact, name='contact'),
    path('admin/', include('adminapp.urls', namespace='admin')),
    path('', include('social_django.urls', namespace='social')),
    path('subadmin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar

    urlpatterns += [re_path(r'^__debug__/', include(debug_toolbar.urls))]