from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.urls import reverse
from .forms import LoginForm, RegisterForm, EditForm
from .models import OnlineshopUser


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activ_key])

    title = f'User confirmation: {user.username}'

    # message = f'To confirm {user.username} on the {settings.DOMAIN_NAME}move: \n\n{settings.DOMAIN_NAME}{verify_link}'
    message = f'To confirm {user.username} on the {settings.DOMAIN_NAME}move: \n\nhttp://127.0.0.1:8000{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activ_key):
    try:
        user = OnlineshopUser.objects.get(email=email)

        if user.activ_key == activ_key and not user.is_activ_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verification.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return redirect('main:main')


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
            # form.save()
            # return redirect(reverse('main:main'))
            user = form.save()
            if send_verify_mail(user):
                print('Message has been sent')
                return redirect('auth:login')
            else:
                print('Error sending the message')
                return redirect('auth:login')

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
