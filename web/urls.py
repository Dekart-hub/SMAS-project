from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path

from web.views import main_view


urlpatterns = [
    path("", main_view),
]
