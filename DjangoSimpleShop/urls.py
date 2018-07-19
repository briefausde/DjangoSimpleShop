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
    url(r'^^(?P<pk>[0-9]+)/edit/$', views.ProductEdit.as_view(), name='product_edit'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home.as_view(), name='home'),
    path('product/', include(product_urls)),
]
