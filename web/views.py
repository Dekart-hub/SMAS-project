import random

from django.http import HttpResponse
from django.shortcuts import render
from matplotlib import pyplot as plt

from web.forms import RegistrationForm
from web.models import StockInformation, User, UserProfile
from web.services import take_data


def main_view(request):
    random_stock = random.choice(StockInformation.objects.prefetch_related('market', 'type').all())
    return render(request, 'web/main.html', {'random_stock': random_stock})


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
