"""DjangoSimpleShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from engine import views

product_urls = [
    url(r'^(?P<pk>[0-9]+)/$', views.ProductDetail.as_view(), name='product_detail'),
    url(r'^create/$', views.ProductCreate.as_view(), name='product_create'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.ProductEdit.as_view(), name='product_edit'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home.as_view(), name='home'),
    path('product/', include(product_urls)),
    path('cart/add', views.CartItemCreate.as_view(), name="add_to_cart"),
    path('cart/remove', views.CartItemDelete.as_view(), name="remove_from_cart"),
    path('cart/', views.CartItemsList.as_view(), name="cart"),
    path('buy/', views.OrderCreate.as_view(), name="buy"),
    path('orders/', views.OrderList.as_view(), name="orders"),
    url(r'^order/processing/(?P<pk>[0-9]+)/$', views.OrderProcessing.as_view(), name='order_processing'),
    url(r'^order/(?P<key>[-\w]+)/$', views.OrderDetail.as_view(), name='order_detail')
]
