from django import forms
from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'name',
            'img_small',
            'img_big',
            'description',
            'amount',
            'price',
            'category',
        )