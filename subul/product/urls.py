from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.ProductRegister.as_view(),name='productRegister'),
    path('list',views.ProductList.as_view(),name='productList'),
]