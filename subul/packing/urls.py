from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.PackingReg.as_view(), name='packingReg'),
    # path('list', views.OrderList.as_view(), name='eggsList'),
]
