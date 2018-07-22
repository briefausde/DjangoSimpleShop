from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


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


class PaymentType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class DeliveryType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class OrderStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    payment_method = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    delivery_method = models.ForeignKey(DeliveryType, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    patronymic = models.CharField(max_length=64, blank=True)
    address = models.CharField(max_length=300, blank=True)
    email = models.EmailField(max_length=128)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Number must be entered in the format: '+999999999'")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    comment = models.TextField(max_length=2000, blank=True)
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    status = models.ForeignKey(OrderStatus, null=True, on_delete=models.CASCADE)
    key = models.CharField(max_length=64, editable=False, blank=True)

    def __str__(self):
        return "{} by {}".format(self.pk, self.email)


class OrderedProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return "{} ordered {}".format(self.order.email, self.product.name)
