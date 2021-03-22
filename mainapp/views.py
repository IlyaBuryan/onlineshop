from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CommentForm
from .models import Category, Product, Comment
import json
import random


def main(request):
    products = Product.objects.filter(number__gte=700).order_by('?')[:10]

    context = {
        'title': 'grocery store',
        'products': products,
    }
    return render(request, 'mainapp/index.html', context)


def get_hot_product():
    pks = Product.objects.values_list('pk', flat=True)
    random_pk = random.choice(pks)
    product_hot = get_object_or_404(Product, pk=random_pk)
    return product_hot


def products(request):
    hot = get_hot_product()
    categories_list = Category.objects.all()
    other = Product.objects.all().exclude(name=f'{hot.name}').order_by('?')[:10]

    context = {
        'title': 'Products',
        'categories_list': categories_list,
        'product_hot': hot,
        'other': other,
    }
    return render(request, 'mainapp/products.html', context)


def category(request, pk):
    page = request.GET.get('page', 1)
    categories_list = Category.objects.all()
    if pk == 0:
        title = 'All products'
        products = Product.objects.all()
        category = {
            'pk': 0,
            'name': 'all',
        }
    else:
        products = Product.objects.filter(category__id=pk).order_by('?')
        category = get_object_or_404(Category, pk=pk)
        title = category

    paginator = Paginator(products, 4)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': title,
        'categories_list': categories_list,
        'products': products_paginator,
        'category': category,
    }
    return render(request, 'mainapp/category.html', context)


def single(request, pk):
    categories_list = Category.objects.all()
    product = get_object_or_404(Product, pk=pk)
    simular = product.category.product_set.all().exclude(name=f'{product.name}').order_by('?')[:5]
    feedbacks = product.comment_set.all()

    context = {
        'title': product.name,
        'categories_list': categories_list,
        'product': product,
        'simular': simular,
        'feedbacks': feedbacks,
    }

    return render(request, 'mainapp/single_product.html', context)


@login_required
def reviews(request, pk):
    categories_list = Category.objects.all()
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = CommentForm(initial={'user': request.user.pk, 'product': product.pk})

    context = {
        'title': product.name,
        'categories_list': categories_list,
        'product': product,
        'form': form
    }

    return render(request, 'mainapp/reviews.html', context)


def contacts(request):
    with open("json/jsonobj.json", 'r', encoding='utf-8') as file:
        stores = json.load(file)
        random.shuffle(stores)

    context = {
        'title': 'contacts',
        'stores': stores,
    }
    return render(request, 'mainapp/contacts.html', context)


def search(request):
    text = request.GET.get('products')
    page = request.GET.get('page', 1)

    categories_list = Category.objects.all()

    if text:
        products = Product.objects.filter(name__contains=f'{text}')
    else:
        return redirect('main:main')

    paginator = Paginator(products, 4)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': 'search',
        'products': products_paginator,
        'categories_list': categories_list,
        'text': text,
    }

    return render(request, 'mainapp/search.html', context)
