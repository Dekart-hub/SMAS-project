import random

from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from matplotlib import pyplot as plt

from web.forms import RegistrationForm, AuthorizationForm
from web.models import StockInformation, User, UserProfile
from web.services import take_data


def main_view(request):
    random_stock = random.choice(StockInformation.objects.prefetch_related('market', 'type').all())
    return render(request, 'web/main.html', {'stock': random_stock})


def plot_pic(request, tag):
    take_data(tag)
    response = HttpResponse(content_type="image/jpeg")
    plt.savefig(response, format="png")
    plt.clf()
    return response


def registration_view(request):
    is_success = False
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email']
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            user_profile = UserProfile(
                user=user,
                avatar=form.cleaned_data['avatar']
            )
            user_profile.save()
            is_success = True
    return render(request, 'web/registration.html', {
        'form': form,
        'is_success': is_success
    })


def authorization_view(request):
    form = AuthorizationForm()
    if request.method == 'POST':
        form = AuthorizationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is None:
                form.add_error(None, 'Введены неверные данные')
            else:
                login(request, user)
                return redirect('main')
    return render(request, 'web/authorization.html', {'form': form})


def stock_view(request, id):
    stock = StockInformation.objects.filter(id=id).first()
    return render(request, 'web/main.html', {'stock': stock})
