from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class OnlineshopUser(AbstractUser):
    age = models.PositiveSmallIntegerField(verbose_name='age')
    city = models.CharField(verbose_name='city', max_length=50, blank=True)
    avatar = models.ImageField(verbose_name='your picture', upload_to='avatars', blank=True)
    email = models.EmailField(default=None, blank=False)

    activ_key = models.CharField(max_length=128, blank=True)
    activ_key_expires = models.DateTimeField(default=now() + timedelta(hours=24))

    def is_activ_key_expired(self):
        if now() < self.activ_key_expires:
            return False
        return True

    def basket_qt(self):
        return sum(i.quantity for i in self.basket_set.all())

    def basket_price(self):
        return sum(i.product.price * i.quantity for i in self.basket_set.all())
