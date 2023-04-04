from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField()


class StockMarket(models.Model):
    title = models.CharField(max_length=50)
    tag = models.CharField(max_length=8)
    description = models.CharField(max_length=500, default='-')


class StockType(models.Model):
    title = models.CharField(max_length=15)
    description = models.CharField(max_length=500, default='-')


class StockInformation(models.Model):
    title = models.CharField(max_length=20)
    tag = models.CharField(max_length=8)
    description = models.CharField(max_length=500, default='-')
    market = models.ForeignKey(StockMarket, on_delete=models.CASCADE)
    type = models.ForeignKey(StockType, on_delete=models.CASCADE)


class Stock(models.Model):
    ts = models.DateTimeField()
    open = models.DecimalField(max_digits=14, decimal_places=4)
    high = models.DecimalField(max_digits=14, decimal_places=4)
    low = models.DecimalField(max_digits=14, decimal_places=4)
    close = models.DecimalField(max_digits=14, decimal_places=4)
    volume = models.IntegerField()
    stock = models.ForeignKey(StockInformation, on_delete=models.CASCADE)


class CustomTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    template = models.JSONField()
