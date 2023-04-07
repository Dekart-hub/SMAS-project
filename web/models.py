from django.db import models
from django.contrib.auth.models import User


TEXT_LENGTH = 500
TITLE_LENGTH = 25
TAG_LENGTH = 8
PRICE_LENGTH = 14
DECIMAL_PRICE_LENGTH = 4


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Аватарка')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class StockMarket(models.Model):
    title = models.CharField(max_length=TITLE_LENGTH, verbose_name='Название')
    tag = models.CharField(max_length=TAG_LENGTH, verbose_name='Тэг')
    description = models.CharField(max_length=TEXT_LENGTH, default=None, verbose_name='Описание')

    class Meta:
        verbose_name = 'Биржа'
        verbose_name_plural = 'Биржи'


class StockType(models.Model):
    title = models.CharField(max_length=TITLE_LENGTH, verbose_name='Название')
    description = models.CharField(max_length=TEXT_LENGTH, default=None, verbose_name='Описание')

    class Meta:
        verbose_name = 'Тип ценной бумаги'
        verbose_name_plural = 'Типы ценных бумаг'


class StockInformation(models.Model):
    title = models.CharField(max_length=TITLE_LENGTH, verbose_name='Название')
    tag = models.CharField(max_length=TAG_LENGTH, verbose_name='Тэг')
    description = models.CharField(max_length=TEXT_LENGTH, default=None, verbose_name='Описание')
    market = models.ForeignKey(StockMarket, on_delete=models.CASCADE, verbose_name='Биржа')
    type = models.ForeignKey(StockType, on_delete=models.CASCADE, verbose_name='Тип бумаги')

    class Meta:
        verbose_name = 'Сводка по бумаге'
        verbose_name_plural = 'Сводки по бумагам'


class Stock(models.Model):
    date = models.DateTimeField(verbose_name='Дата')
    open = models.DecimalField(max_digits=PRICE_LENGTH,
                               decimal_places=DECIMAL_PRICE_LENGTH,
                               verbose_name='Цена открытия')
    high = models.DecimalField(max_digits=PRICE_LENGTH,
                               decimal_places=DECIMAL_PRICE_LENGTH,
                               verbose_name='Максимальная цена')
    low = models.DecimalField(max_digits=PRICE_LENGTH,
                              decimal_places=DECIMAL_PRICE_LENGTH,
                              verbose_name='Минимальная цена')
    close = models.DecimalField(max_digits=PRICE_LENGTH,
                                decimal_places=DECIMAL_PRICE_LENGTH,
                                verbose_name='Цена закрытия', default=None, null=True)
    volume = models.IntegerField(verbose_name='Объём продаж')
    stock = models.ForeignKey(StockInformation, on_delete=models.CASCADE,
                              verbose_name='Ценная бумага')

    class Meta:
        verbose_name = 'Ценная бумага'
        verbose_name_plural = 'Ценные бумаги'


class CustomTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    template = models.JSONField(verbose_name='Шаблон в формате JSON')

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'
