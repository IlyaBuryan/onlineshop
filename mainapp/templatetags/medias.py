from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='media_folder')
def media_folder(string):
    return f'{settings.MEDIA_URL}{string}'
