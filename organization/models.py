from django.db import models

from base.constants import AssetStatusChoices
from base.models import BaseModel


# Create your models here.

class Subsidiary(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Currency(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=50)
    exchange_rate = models.DecimalField(max_digits=15, decimal_places=6)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Asset(BaseModel):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    subsidiary = models.ForeignKey('Subsidiary', on_delete=models.CASCADE)
    acquisition_date = models.DateField(blank=True, null=True)
    cost = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    currency = models.ForeignKey('Currency', on_delete=models.SET_DEFAULT, default='USD')
    status = models.CharField(max_length=50, choices=AssetStatusChoices.choices, default=AssetStatusChoices.ACTIVE)

    def __str__(self):
        return self.name
