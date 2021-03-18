from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from basketapp.models import Basket


@login_required
def index(request):
    basket = request.user.basket_set.all()

    context = {
        'title': 'basket',
        'basket': basket,
    }

    return render(request, 'basketapp/index.html', context)


@login_required
def add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return redirect(reverse('main:single', args=[pk]))

    basket_product, _ = Basket.objects.get_or_create(user=request.user, product_id=pk)
    basket_product.quantity += 1
    basket_product.save()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def remove(request, item_pk):
    basket_item = get_object_or_404(Basket, pk=item_pk)
    basket_item.delete()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def update(request, pk, num):
    if request.is_ajax():
        item = Basket.objects.filter(pk=pk).first()

        if num == 0:
            item.delete()
        else:
            item.quantity = num
            item.save()

        basket = request.user.basket_set.all()

        context = {
            'basket': basket
        }

        result = render_to_string('basketapp/basket_list.html', context, request=request)

        return JsonResponse({'result': result})
