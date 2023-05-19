from django.http import HttpResponse
from django.shortcuts import render
from matplotlib import pyplot as plt

from web.services import take_data


def main_view(request):
    return render(request, 'web/main.html')


def plot_pic(request):
    take_data('IBM')
    response = HttpResponse(content_type="image/jpeg")
    plt.savefig(response, format="png")
    plt.clf()
    return response
