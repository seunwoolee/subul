from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    # path('',views.ProductRegister.as_view(),name='orderRegister'),
    path('list',views.OrderList.as_view(),name='orderList'),
]