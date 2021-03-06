from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete

from basketapp.models import Basket
from mainapp.models import Product
from .forms import OrderItemForm
from .models import Order, OrderItem


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


class OrderList(CheckAuthMixin, ContextDataMixin, ListView):
    model = Order
    title = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderItemsCreate(CheckAuthMixin, ContextDataMixin, CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:orders_list')
    title = 'order'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=3)

        # Первый позиционный аргумент - родительский класс, второй - класс, на основе которого
        # будет создаваться набор форм класса, указанного в именованномаргументе «form = OrderItemForm».

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items.exists():
                OrderFormSet = inlineformset_factory(Order, OrderItem,
                                                     form=OrderItemForm,
                                                     extra=len(basket_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
            else:
                formset = OrderFormSet()

        data['orderitems'] = formset

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
                Basket.objects.filter(user=self.request.user).delete()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderItemsUpdate(CheckAuthMixin, ContextDataMixin, UpdateView):
    model = Order
    fields = []
    title = 'order'

    def get_success_url(self):
        return reverse_lazy('order:order_update', kwargs={
            'pk': self.object.pk,
        })

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        # Первый позиционный аргумент - родительский класс, второй - класс, на основе которого
        # будет создаваться набор форм класса, указанного в именованномаргументе «form = OrderItemForm».

        if self.request.POST:
            data['orderitems'] = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
            data['orderitems'] = formset

            # data['orderitems'] = OrderFormSet(instance=self.object)

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderDelete(CheckAuthMixin, ContextDataMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('order:orders_list')
    title = 'delete'


class OrderRead(CheckAuthMixin, ContextDataMixin, DetailView):
    model = Order
    title = 'read'


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return redirect('ordersapp:orders_list')


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    if update_fields is 'quantity' or 'product':
        if instance.pk:
            instance.product.number -= instance.quantity - sender.get_item(instance.pk).quantity
        else:
            instance.product.number -= instance.quantity
        instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.number += instance.quantity
    instance.product.save()


def get_prod_price(request, pk):
    if request.is_ajax():
        product_item = Product.objects.filter(pk=int(pk)).first()
        if product_item:
            return JsonResponse({'price': product_item.price})
        return JsonResponse({'price': 0})
