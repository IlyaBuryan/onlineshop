from django.db import models

from django.conf import settings

from basketapp.models import Basket
from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    COMPLETED = 'CM'
    CANCELLED = 'CNC'

    ORDERS_STATUS_CHOICES = (
        (FORMING, 'Forming'),
        (SENT_TO_PROCEED, 'Proceeding'),
        (PROCEEDED, 'Proceeded'),
        (PAID, 'Paid'),
        (READY, 'Ready'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=3, choices=ORDERS_STATUS_CHOICES, default=FORMING)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.pk

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return len(items)

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity * x.product.price, items)))

    def delete(self):
        for item in self.orderitems.select_related():
            item.product.number += item.quantity
            item.product.save()

        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name="orderitems",
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                verbose_name='Product',
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Quantity',
                                           default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.filter(pk=pk).first()