from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import reverse
from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm
from django.shortcuts import get_object_or_404, render
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from authapp.models import ShopUser
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_product_category_save(sender, instance, **kwargs):
    print(f"{sender=}")
    print(f"{instance=}")
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)


class UserListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def user_create(request):
    title = 'пользователи/создание'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        user_form = ShopUserRegisterForm()

    content = {'title': title, 'update_form': user_form}

    return render(request, 'adminapp/user_update.html', content)


def user_update(request, pk):
    title = 'пользователи/редактирование'

    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:user_update', args=[edit_user.pk]))
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)

    content = {'title': title, 'update_form': edit_form}

    return render(request, 'adminapp/user_update.html', content)


def user_delete(request, pk):
    title = 'пользователи/удаление'
    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('admin:users'))

    content = {'title': title, 'user_to_delete': user}

    return render(request, 'adminapp/user_delete.html', content)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/categories_update.html'
    success_url = reverse_lazy('admin:categories')
    fields = '__all__'


class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/categories_update.html'
    success_url = reverse_lazy('admin:categories')
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)
                print(f'{self.__class__}')

        return super().form_valid(form)


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')

    def form_valid(self, form):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('admin:products')
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('admin:products', args=[self.object.category.pk])


class ProductsListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/продукты'
        context['category'] = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        context['objects'] = Product.objects.filter(category__pk=self.kwargs['pk']).order_by('name')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(category__pk=self.kwargs['pk'])


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('admin:products')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/редактирование'
        return context

    def get_success_url(self):
        return reverse_lazy('admin:products', args=[self.object.category.pk])


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'
    success_url = reverse_lazy('admin:products')
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('admin:products', args=[self.object.category.pk])

    def form_valid(self, form):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
