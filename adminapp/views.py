from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mainapp.models import Product, Category
from adminapp.forms import ShopUserAdminUpdateForm, ShopUserAdminCreateForm

# Users
"""
@user_passes_test(lambda i: i.is_superuser)
def users_read(request):
    title = 'admin:users'

    users_list = OnlineshopUser.objects.all().order_by('-is_active',
                                                       '-is_superuser',
                                                       '-is_staff')

    context = {
        'title': title,
        'users_list': users_list,
    }

    return render(request, 'adminapp/users_read.html', context)

@user_passes_test(lambda i: i.is_superuser)
def users_create(request):
    title = 'users:creation'

    if request.method == 'POST':
        user_form = RegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return redirect(reverse('useradmin:users_read'))
    else:
        user_form = RegisterForm()

    content = {
        'title': title,
        'update_form': user_form
    }

    return render(request, 'adminapp/user_admin.html', content)


@user_passes_test(lambda i: i.is_superuser)
def users_update(request, user_pk):
    title = 'users:edit'

    edit_user = get_object_or_404(OnlineshopUser, pk=user_pk)
    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return redirect(reverse('useradmin:users_read'))
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)

    content = {
        'title': title,
        'update_form': edit_form
    }

    return render(request, 'adminapp/user_admin.html', content)


@user_passes_test(lambda i: i.is_superuser)
def users_delete(request, user_pk):
    title = 'users:delete'

    user = get_object_or_404(OnlineshopUser, pk=user_pk)

    if request.method == 'POST':
        user.is_active = False
        user.save()
        return redirect(reverse('useradmin:users_read'))

    content = {
        'title': title,
        'user_to_delete': user
    }

    return render(request, 'adminapp/user_admin.html', content)
"""


class CheckSuperuserMixin:
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CheckAuthMixin:
    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ContextDataMixin:
    title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class SuccessUrlMixin:

    def get_success_url(self):
        return reverse('useradmin:products_read', kwargs={
            'category_pk': self.kwargs['category_pk']
        })


class UsersListView(CheckAuthMixin, ContextDataMixin, ListView):
    model = get_user_model()
    queryset = get_user_model().objects.all().order_by('-is_active',
                                                       'username')
    template_name = 'adminapp/user_admin.html'
    title = 'admin:users'


class UsersCreate(CheckAuthMixin, ContextDataMixin, CreateView):
    form_class = ShopUserAdminCreateForm
    template_name = 'adminapp/user_admin.html'
    title = 'users:creation'
    success_url = reverse_lazy('useradmin:users_read')


class UsersUpdate(CheckAuthMixin, UpdateView):
    form_class = ShopUserAdminUpdateForm
    template_name = 'adminapp/user_admin.html'
    success_url = reverse_lazy('useradmin:users_read')

    pk_url_kwarg = 'user_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'users:update'
        context['user_pk'] = self.kwargs['user_pk']
        return context

    def get_queryset(self):
        return get_user_model().objects.all()


class UsersDelete(CheckAuthMixin, ContextDataMixin, DeleteView):
    model = get_user_model()
    template_name = 'adminapp/user_admin.html'
    title = 'users:delete'
    success_url = 'adminapp:users_read'

    pk_url_kwarg = 'user_pk'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return redirect(self.get_success_url())


# Categories
"""
@user_passes_test(lambda i: i.is_superuser)
def categories_read(request):
    title = 'admin:categories'

    categories_list = Category.objects.all().order_by('name')

    context = {
        'title': title,
        'categories_list': categories_list,
    }

    return render(request, 'adminapp/categories_read.html', context)
"""


class CategoriesListView(CheckAuthMixin, ContextDataMixin, ListView):
    model = Category
    template_name = 'adminapp/categories_admin.html'
    title = 'admin:categories'


class CategoriesCreate(CheckSuperuserMixin, ContextDataMixin, CreateView):
    model = Category
    fields = '__all__'
    template_name = 'adminapp/categories_admin.html'
    title = 'categories:creation'
    success_url = reverse_lazy('useradmin:categories_read')


class CategoriesUpdate(CheckSuperuserMixin, ContextDataMixin, UpdateView):
    model = Category
    fields = '__all__'
    title = 'categories:update'
    template_name = 'adminapp/categories_admin.html'
    success_url = reverse_lazy('useradmin:categories_read')

    pk_url_kwarg = 'category_pk'


class CategoriesDelete(CheckSuperuserMixin, ContextDataMixin, DeleteView):
    model = Category
    title = 'categories:delete'
    fields = '__all__'
    template_name = 'adminapp/categories_admin.html'
    success_url = reverse_lazy('useradmin:categories_read')

    pk_url_kwarg = 'category_pk'


# Products

"""
@user_passes_test(lambda i: i.is_superuser)
def products_read(request, category_pk):
    title = 'admin:products'

    category = get_object_or_404(Category, pk=category_pk)
    products_list = category.product_set.all().order_by('name')

    content = {
        'title': title,
        'category': category,
        'products_list': products_list,
    }

    return render(request, 'adminapp/products_read.html', content)
"""


class ProductsListView(CheckAuthMixin, ListView):
    model = Product
    template_name = 'adminapp/products_admin.html'

    pk_url_kwarg = 'category_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'admin:products'
        context['category_pk'] = self.kwargs['category_pk']
        return context

    def get_queryset(self):
        pk = self.kwargs['category_pk']
        self.object = get_object_or_404(Category, pk=pk)
        products_list = self.object.product_set.all().order_by('name')
        return products_list


class ProductsCreate(CheckSuperuserMixin, SuccessUrlMixin, CreateView):
    model = Product
    fields = '__all__'
    template_name = 'adminapp/products_admin.html'

    pk_url_kwarg = 'category_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'products:create'
        context['category_pk'] = self.kwargs['category_pk']
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['category'] = self.kwargs['category_pk']
        return initial


class ProductsUpdate(CheckSuperuserMixin, SuccessUrlMixin, UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'adminapp/products_admin.html'

    pk_url_kwarg = 'product_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'products:update'
        context['category_pk'] = self.kwargs['category_pk']
        return context


class ProductsDelete(CheckSuperuserMixin, SuccessUrlMixin, DeleteView):
    model = Product
    fields = '__all__'
    template_name = 'adminapp/products_admin.html'

    pk_url_kwarg = 'product_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'products:delete'
        context['category_pk'] = self.kwargs['category_pk']
        return context


class ProductView(CheckAuthMixin, ContextDataMixin, DetailView):
    model = Product
    title = 'product'
    template_name = 'adminapp/single_product.html'

    pk_url_kwarg = 'product_pk'
