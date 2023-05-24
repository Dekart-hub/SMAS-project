from django.urls import path

from web.views import main_view, plot_pic, registration_view, authorization_view, stock_view, stocks_view

urlpatterns = [
    path('', main_view, name='main'),
    path('pic/<str:tag>', plot_pic, name='plot_pic'),
    path('registration/', registration_view, name='registration'),
    path('authorization/', authorization_view, name='authorization'),
    path('stock/<int:id>', stock_view, name='stock'),
    path('stocks/', stocks_view, name='stocks'),
]
