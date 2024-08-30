from typing import TYPE_CHECKING

from django.db import models
from django.db.models import Manager


class Category(models.Model):
    name = models.CharField(max_length=250)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='subcategories',
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name

    if TYPE_CHECKING:
        objects: Manager


class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    image = models.ImageField(upload_to='products/images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    characteristics = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name

    if TYPE_CHECKING:
        objects: Manager
