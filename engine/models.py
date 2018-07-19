from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class ProductCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    img_small = models.CharField(max_length=500, default="/static/media/small_default_image.jpg", blank=True)
    img_big = models.CharField(max_length=500, default="/static/media/big_default_image.jpg", blank=True)
    description = models.TextField(max_length=20000)
    amount = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0, blank=True)
    tags = models.CharField(max_length=300, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    published_date = models.DateTimeField(blank=True, null=True, editable=False)
    views = models.PositiveIntegerField(default=0, editable=False)
    url = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.name
