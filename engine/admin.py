from django.contrib import admin
from .models import Product, ProductCategory, Order, DeliveryType, PaymentType


admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Order)
admin.site.register(DeliveryType)
admin.site.register(PaymentType)
