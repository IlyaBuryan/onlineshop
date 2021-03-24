from django.core.management.base import BaseCommand
from authapp.models import OnlineshopUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        super_user = OnlineshopUser.objects.create_user('admin', 'burian-iliyar@yandex.ru', '4253316admin', age=22)
        user = OnlineshopUser.objects.create_user('ilya', 'burian-iliyar@yandex.ru', '4253316ilya', age=22)
