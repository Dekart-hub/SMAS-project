from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Аватарка')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class StockMarket(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    tag = models.CharField(max_length=8, verbose_name='Тэг')
    description = models.CharField(max_length=500, default='-', verbose_name='Описание')

    class Meta:
        verbose_name = 'биржа'
        verbose_name_plural = 'биржи'


class StockType(models.Model):
    title = models.CharField(max_length=15, verbose_name='Название')
    description = models.CharField(max_length=500, default='-', verbose_name='Описание')

    class Meta:
        verbose_name = 'тип ценной бумаги'
        verbose_name_plural = 'типы ценных бумаг'


class StockInformation(models.Model):
    title = models.CharField(max_length=20, verbose_name='Название')
    tag = models.CharField(max_length=8, verbose_name='Тэг')
    description = models.CharField(max_length=500, default='-', verbose_name='Описание')
    market = models.ForeignKey(StockMarket, on_delete=models.CASCADE, verbose_name='Биржа')
    type = models.ForeignKey(StockType, on_delete=models.CASCADE, verbose_name='Тип бумаги')

    class Meta:
        verbose_name = 'сводка по бумаге'
        verbose_name_plural = 'сводки по бумагам'


class Stock(models.Model):
    date = models.DateTimeField(verbose_name='Дата')
    open = models.DecimalField(max_digits=14, decimal_places=4, verbose_name='Цена открытия')
    high = models.DecimalField(max_digits=14, decimal_places=4, verbose_name='Максимальная цена')
    low = models.DecimalField(max_digits=14, decimal_places=4, verbose_name='Минимальная цена')
    close = models.DecimalField(max_digits=14, decimal_places=4, verbose_name='Цена закрытия')
    volume = models.IntegerField(verbose_name='Объём продаж')
    stock = models.ForeignKey(StockInformation, on_delete=models.CASCADE, verbose_name='Ценная бумага')

    class Meta:
        verbose_name = 'ценная бумага'
        verbose_name_plural = 'ценные бумаги'


class CustomTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    template = models.JSONField(verbose_name='Шаблон в формате JSON')

    class Meta:
        verbose_name = 'шаблон'
        verbose_name_plural = 'шаблоны'
