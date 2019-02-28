from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ProductRegister.as_view(), name='productRegister'),
    path('list', views.ProductList.as_view(), name='productList'),
    path('recall/<int:pk>', views.ProductRecall.as_view(), name='productRecall'),
    path('productReport', views.ProductReport.as_view(), name='productReport'),
    path('productOEMReg', views.ProductOEMReg.as_view(), name='productOEMReg'),
    path('productOEMList', views.ProductOEMList.as_view(), name='productOEMList'),
    path('ProductUnitPricesList', views.ProductUnitPricesList.as_view(), name='productUnitPricesList'),
    path('setProductMatchList', views.SetProductMatchList.as_view(), name='setProductMatchList'),
]