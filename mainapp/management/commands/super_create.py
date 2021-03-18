from django.core.management.base import BaseCommand
from authapp.models import OnlineshopUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        super_user = OnlineshopUser.objects.create_user('ilya', 'burian-iliyar@yandex.ru', 'ilya', age=22)
        user = OnlineshopUser.objects.create_user('ilya2', 'burian-iliyar@yandex.ru', 'ilya2', age=22)
