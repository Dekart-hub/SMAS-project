from django.urls import path

from web.views import main_view, plot_pic, registration_view, authorization_view, stock_view, stocks_view, logout_view

urlpatterns = [
    path('', main_view, name='main'),
    path('pic', plot_pic, name='plot_pic'),
    path('registration/', registration_view, name='registration'),
    path('authorization/', authorization_view, name='authorization'),
    path('stock/<int:id>', stock_view, name='stock'),
    path('stocks/', stocks_view, name='stocks'),
    path('logout/', logout_view, name='logout'),
]
