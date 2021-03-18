from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse
from .forms import LoginForm, RegisterForm, EditForm


def login(request):
    log_form = LoginForm(data=request.POST)

    next = request.GET['next'] if 'next' in request.GET.keys() else ''
    # < QueryDict: {'next': ['/basket/add/25']} >

    if request.method == 'POST':
        if log_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user and user.is_active:
                auth.login(request, user)
                if 'next' in request.POST.keys():
                    return redirect(request.POST['next'])
                else:
                    return redirect(reverse('main:main'))

    context = {
        'title': 'login',
        'log_form': log_form,
        'next': next,
    }

    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return redirect(reverse('main:main'))


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect(reverse('main:main'))
    else:
        form = RegisterForm()

    context = {
        'title': 'register',
        'form': form,
    }
    return render(request, 'authapp/reg_edit.html', context)


def edit(request):
    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('main:main'))
    else:
        form = EditForm(instance=request.user)

    context = {
        'title': 'update',
        'form': form,
    }
    return render(request, 'authapp/reg_edit.html', context)
