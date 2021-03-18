from django.contrib.auth import get_user_model
from django.db import models

from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='number', default=0)
    add_datetime = models.DateTimeField(verbose_name='time', auto_now=True)

    def __str__(self):
        return f'{self.product} ({self.product.category.name})'.upper()

    def product_cost(self):
        cost = self.product.price * self.quantity
        return cost
