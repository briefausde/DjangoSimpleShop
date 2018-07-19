from .models import *
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse
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
    template_name = 'products.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['products'] = self.get_queryset()

        if self.request.session.get('cart_items', False):
            context['cart_items'] = len(self.request.session['cart_items'].split(','))

        return context


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


class AddItemToCart(View):

    def post(self, *args, **kwargs):
        if self.request.session.get('cart_items', False):
            self.request.session['cart_items'] += ',%s' % self.request.POST.get('item')
        else:
            self.request.session['cart_items'] = self.request.POST.get('item')
        return HttpResponse('ok')
