from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView

from basketapp.models import Basket
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
                basket_items.delete()
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

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderItemsUpdate(CheckAuthMixin, ContextDataMixin, UpdateView):
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
            data['orderitems'] = OrderFormSet(self.request.POST, instance=self.object)
        else:
            data['orderitems'] = OrderFormSet(instance=self.object)

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
