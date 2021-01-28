from django.contrib.auth.decorators import user_passes_test
from django.db import connection
from django.db.models import F
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser

# Create your views here.
from mainapp.models import ProductCategories, Product


# def user_create(request):
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin:users'))
#     else:
#         user_form = ShopUserRegisterForm()
#
#     content = {'update_form': user_form}
#     return render(request, 'adminapp/user_update.html', content)


class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    form_class = ShopUserRegisterForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['title'] = 'Пользователь/Создание'
        return content


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     user_list = ShopUser.objects.all().order_by('-is_active')
#     content = {
#         'objects': user_list
#     }
#     return render(request, 'adminapp/users.html', content)


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['title'] = 'Пользователи'
        return content

# def user_update(request, pk):
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin:user_update', args=[edit_user.pk]))
#     else:
#         edit_form = ShopUserAdminEditForm(instance=edit_user)
#
#     content = {'update_form': edit_form}
#     return render(request, 'adminapp/user_update.html', content)


class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    form_class = ShopUserAdminEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['title'] = 'Пользователь/Редактирование'
        return content


# def user_delete(request, pk):
#     delete_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         if delete_user.is_active:
#             delete_user.is_active = False
#             delete_user.save()
#         else:
#             delete_user.is_active = True
#             delete_user.save()
#         return HttpResponseRedirect(reverse('admin:users'))
#
#     content = {
#         'user_to_delete': delete_user
#     }
#     return render(request, 'adminapp/user_delete.html', content)

class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

# def category_create(request):
#     if request.method == 'POST':
#         category_form = ProductCategoryEditForm(request.POST, request.FILES)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('admin:categories'))
#     else:
#         category_form = ProductCategoryEditForm()
#
#     content = {'update_form': category_form}
#     return render(request, 'adminapp/category_update.html', content)


class ProductCategoryCreateView(CreateView):
    model = ProductCategories
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['title'] = 'Категории/Создание'
        return content

# def categories(request):
#     category_list = ProductCategories.objects.all().order_by('-is_active')
#     content = {
#         'objects': category_list
#     }
#     return render(request, 'adminapp/categories.html', content)


class ProductCategoryListView(ListView):
    model = ProductCategories
    template_name = 'adminapp/categories.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['title'] = 'Категории'
        return content

# def category_update(request, pk):
#     edit_category = get_object_or_404(ProductCategories, pk=pk)
#     if request.method == 'POST':
#         edit_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin:category_update', args=[edit_category.pk]))
#     else:
#         edit_form = ProductCategoryEditForm(instance=edit_category)
#
#     content = {'update_form': edit_form}
#     return render(request, 'adminapp/category_update.html', content)


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategories
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['title'] = 'Категории/Редактирование'
        return content

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)


# def category_delete(request, pk):
#     delete_category = get_object_or_404(ProductCategories, pk=pk)
#     if request.method == 'POST':
#         if delete_category.is_active:
#             delete_category.is_active = False
#             delete_category.save()
#         else:
#             delete_category.is_active = True
#             delete_category.save()
#         return HttpResponseRedirect(reverse('admin:categories'))
#
#     content = {
#         'category_to_delete': delete_category
#     }
#     return render(request, 'adminapp/category_delete.html', content)

class ProductCategoryDeleteView(DeleteView):
    model = ProductCategories
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# def product_create(request, pk):
#     category = get_object_or_404(ProductCategories, pk=pk)
#
#     if request.method == 'POST':
#         product_form = ProductEditForm(request.POST, request.FILES)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(reverse('admin:products', args=[pk]))
#     else:
#         product_form = ProductEditForm(initial={'category': category})
#
#     content = {
#         'update_form': product_form,
#         'category': category
#     }
#
#     return render(request, 'adminapp/product_update.html', content)

class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    form_class = ProductEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['title'] = 'Продукт/Редактирование'
        content['category'] = self.kwargs['pk']
        return content

    def get_success_url(self):
        return reverse_lazy('admin:products', args=[self.kwargs['pk']])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        print(kwargs)
        category_item = get_object_or_404(ProductCategories, pk=self.kwargs['pk'])
        kwargs['initial'] = {'category': category_item}
        return kwargs

# def products(request, pk):
#     category_item = get_object_or_404(ProductCategories, pk=pk)
#     product_list = Product.objects.filter(category=category_item)
#     content = {
#         'objects': product_list,
#         'category': category_item
#     }
#     return render(request, 'adminapp/products.html', content)


class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['title'] = 'Категории'
        content['category'] = get_object_or_404(ProductCategories, pk=self.kwargs['pk'])
        return content

    def get_queryset(self):
        category_pk = self.kwargs['pk']
        return Product.objects.filter(category_id=category_pk)


# def product_read(request, pk):
#     title = 'продукт/подробнее'
#     product = get_object_or_404(Product, pk=pk)
#     content = {'title': title, 'object': product, }
#
#     return render(request, 'adminapp/product_read.html', content)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['title'] = 'Категории/Редактирование'
        return content


# def product_update(request, pk):
#     edit_product = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin:product_update', args=[edit_product.pk]))
#     else:
#         edit_form = ProductEditForm(instance=edit_product)
#
#     content = {
#         'update_form': edit_form,
#         'category': edit_product.category
#     }
#
#     return render(request, 'adminapp/product_update.html', content)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    form_class = ProductEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['title'] = 'Продукт/Редактирование'
        update_product = get_object_or_404(Product, pk=self.kwargs['pk'])
        content['category'] = update_product.category.pk
        return content

    def get_success_url(self):
        update_product = get_object_or_404(Product, pk=self.kwargs['pk'])
        return reverse_lazy('admin:products', args=[update_product.category.pk])


# def product_delete(request, pk):
#     delete_product = get_object_or_404(Product, pk=pk)
#     if request.method == 'POST':
#         if delete_product.is_active:
#             delete_product.is_active = False
#             delete_product.save()
#         else:
#             delete_product.is_active = True
#             delete_product.save()
#         return HttpResponseRedirect(reverse('admin:products', args=[delete_product.category.pk]))
#
#     content = {
#         'product_to_delete': delete_product
#     }
#     return render(request, 'adminapp/product_delete.html', content)

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        delete_product = get_object_or_404(Product, pk=self.kwargs['pk'])
        return reverse_lazy('admin:products', args=[delete_product.category.pk])

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategories)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)
