from .models import *
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from .forms import ProductForm

from django.views.generic import (
    ListView,
    View,
    CreateView,
    UpdateView,
    DetailView
)


class Home(ListView):
    model = Product
    template_name = 'products.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['products'] = self.get_queryset()

        if self.request.session.get('cart_items', False):
            context['cart_items'] = len(self.request.session['cart_items'])

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


class CartItemsList(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'cart.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CartItemsList, self).get_context_data(**kwargs)
        context['price'] = sum([product.price for product in self.get_queryset()])
        return context

    def get_queryset(self):
        if self.request.session.get('cart_items', False):
            return [get_object_or_404(self.model, pk=pk) for pk in self.request.session['cart_items']]
        return []


class CartItemCreate(View):

    def post(self, *args, **kwargs):
        if self.request.session.get('cart_items', False):
            self.request.session['cart_items'].append(int(self.request.POST.get('item')))
            self.request.session.modified = True
        else:
            self.request.session['cart_items'] = [int(self.request.POST.get('item'))]
        return HttpResponse('ok')


class CartItemDelete(View):

    def post(self, *args, **kwargs):
        if self.request.session.get('cart_items', False):
            item = int(self.request.POST.get('item'))
            if item in self.request.session['cart_items']:
                self.request.session['cart_items'].remove(item)
                self.request.session.modified = True
        return HttpResponse('ok')


class OrderCreate(CreateView):
    model = Order
    fields = [
        'payment_method',
        'delivery_method',
        'name', 'surname',
        'patronymic',
        'address',
        'email',
        'phone',
        'comment'
    ]
    template_name = 'form.html'

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data(**kwargs)
        products = self.get_queryset()
        context['ordered_products'] = products
        context['ordered_products_price'] = sum([product.price for product in products])
        return context

    def get_success_url(self):
        items = self.get_queryset()
        if items:
            for item in items:
                OrderedProduct.objects.create(order=self.object, product=item)
            del self.request.session['cart_items']
        return '/'

    def get_queryset(self):
        if self.request.session.get('cart_items', False):
            return [get_object_or_404(Product, pk=pk) for pk in self.request.session['cart_items']]
        return []


class OrderList(ListView):
    model = Order
    template_name = 'orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return self.model.objects.filter(executed=False)


class OrderDetail(DetailView):
    model = Order
    template_name = 'order_detail.html'

    def get_context_data(self, **kwargs):
        context = super(OrderDetail, self).get_context_data()
        order = self.get_object()
        context['order'] = order
        context['products'] = OrderedProduct.objects.filter(order=order)
        return context

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs['pk'])
