from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser

# Create your views here.
from mainapp.models import ProductCategories, Product


def user_create(request):
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        user_form = ShopUserRegisterForm()

    content = {'update_form': user_form}
    return render(request, 'adminapp/user_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    user_list = ShopUser.objects.all().order_by('-is_active')
    content = {
        'objects': user_list
    }
    return render(request, 'adminapp/users.html', content)


def user_update(request, pk):
    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:user_update', args=[edit_user.pk]))
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)

    content = {'update_form': edit_form}
    return render(request, 'adminapp/user_update.html', content)


def user_delete(request, pk):
    delete_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        if delete_user.is_active:
            delete_user.is_active = False
            delete_user.save()
        else:
            delete_user.is_active = True
            delete_user.save()
        return HttpResponseRedirect(reverse('admin:users'))

    content = {
        'user_to_delete': delete_user
    }
    return render(request, 'adminapp/user_delete.html', content)


def category_create(request):
    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin:categories'))
    else:
        category_form = ProductCategoryEditForm()

    content = {'update_form': category_form}
    return render(request, 'adminapp/category_update.html', content)


def categories(request):
    category_list = ProductCategories.objects.all().order_by('-is_active')
    content = {
        'objects': category_list
    }
    return render(request, 'adminapp/categories.html', content)


def category_update(request, pk):
    edit_category = get_object_or_404(ProductCategories, pk=pk)
    if request.method == 'POST':
        edit_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:category_update', args=[edit_category.pk]))
    else:
        edit_form = ProductCategoryEditForm(instance=edit_category)

    content = {'update_form': edit_form}
    return render(request, 'adminapp/category_update.html', content)


def category_delete(request, pk):
    delete_category = get_object_or_404(ProductCategories, pk=pk)
    if request.method == 'POST':
        if delete_category.is_active:
            delete_category.is_active = False
            delete_category.save()
        else:
            delete_category.is_active = True
            delete_category.save()
        return HttpResponseRedirect(reverse('admin:categories'))

    content = {
        'category_to_delete': delete_category
    }
    return render(request, 'adminapp/category_delete.html', content)


def product_create(request, pk):
    category = get_object_or_404(ProductCategories, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin:products', args=[pk]))
    else:
        product_form = ProductEditForm(initial={'category': category})

    content = {
               'update_form': product_form,
               'category': category
               }

    return render(request, 'adminapp/product_update.html', content)


def products(request, pk):
    category_item = get_object_or_404(ProductCategories, pk=pk)
    product_list = Product.objects.filter(category=category_item)
    content = {
        'objects': product_list,
        'category': category_item
    }
    return render(request, 'adminapp/products.html', content)


def product_read(request, pk):
    pass


def product_update(request, pk):
    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:product_update', args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)

    content = {
               'update_form': edit_form,
               'category': edit_product.category
               }

    return render(request, 'adminapp/product_update.html', content)


def product_delete(request, pk):
    delete_product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        if delete_product.is_active:
            delete_product.is_active = False
            delete_product.save()
        else:
            delete_product.is_active = True
            delete_product.save()
        return HttpResponseRedirect(reverse('admin:products', args=[delete_product.category.pk]))

    content = {
        'product_to_delete': delete_product
    }
    return render(request, 'adminapp/product_delete.html', content)
