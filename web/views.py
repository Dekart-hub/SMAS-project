import random

from django.http import HttpResponse
from django.shortcuts import render
from matplotlib import pyplot as plt

from web.models import StockInformation
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
