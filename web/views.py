import random

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from matplotlib import pyplot as plt

from web.forms import RegistrationForm, AuthorizationForm, StockFilterForm, GraphForm
from web.models import StockInformation, User, UserProfile
from web.services import take_data, filter_stocks, get_stock_data


def main_view(request):
    random_stock = random.choice(StockInformation.objects.all())
    filters = {'model': None, 'start_date': None, 'end_date': None}
    take_data(random_stock.tag, filters)
    return render(request, 'web/main.html', {
        'stock': random_stock,
        'stock_view': False
    })


def plot_pic(request):
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


@login_required
def stock_view(request, id):
    stock = StockInformation.objects.filter(id=id).first()
    filters = {'model': None, 'start_date': None, 'end_date': None}
    form = GraphForm()
    if request.method == 'POST':
        form = GraphForm(data=request.POST)
        if form.is_valid():
            filters = form.cleaned_data
    take_data(stock.tag, filters)
    return render(request, 'web/main.html', {
        'stock': stock,
        'form': form,
        'stock_view': True
    })


@login_required
def stocks_view(request):
    stocks = StockInformation.objects.select_related('market', 'type').all()
    filter_form = StockFilterForm()
    if request.method == 'POST':
        filter_form = StockFilterForm(data=request.POST)
        if filter_form.is_valid():
            stocks = filter_stocks(stocks, filter_form.cleaned_data)
    stocks_data = get_stock_data(stocks)
    print(stocks_data)
    return render(request, 'web/stocks.html', {
        'stocks': stocks,
        'filter_form': filter_form,
        'stocks_data': stocks_data
    })


def logout_view(request):
    logout(request)
    return redirect('main')
