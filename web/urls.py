from django.urls import path

from web.views import main_view, plot_pic

urlpatterns = [
    path('', main_view, name='main'),
    path('pic/', plot_pic, name='plot_pic'),
]
