from django.db import models
from django.contrib.auth.models import AbstractUser


class OnlineshopUser(AbstractUser):
    age = models.PositiveSmallIntegerField(verbose_name='age')
    city = models.CharField(verbose_name='city', max_length=50, blank=True)
    avatar = models.ImageField(verbose_name='your picture', upload_to='avatars', blank=True)

    def basket_qt(self):
        return sum(i.quantity for i in self.basket_set.all())

    def basket_price(self):
        return sum(i.product.price * i.quantity for i in self.basket_set.all())
