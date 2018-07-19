from .models import *
from django.views.generic import (
    TemplateView,
    ListView
)


class Home(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products.html'
