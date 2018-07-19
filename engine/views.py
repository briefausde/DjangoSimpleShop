from .models import *
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .forms import ProductForm

from django.views.generic import (
    ListView,
    View,
    CreateView,
    UpdateView
)


class Home(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products.html'


class ProductDetail(View):
    model = Product

    def get(self, *args, **kwargs):
        product = self.get_object()
        product.views += 1
        product.save()
        return JsonResponse(model_to_dict(product))

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs['pk'])


class ProductCreate(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ProductCreate, self).form_valid(form)


class ProductEdit(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'form.html'

    def get_success_url(self):
        return '/'
