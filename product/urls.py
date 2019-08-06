from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ProductRegister.as_view(), name='productRegister'),
    path('list', views.ProductList.as_view(), name='productList'),
    path('order', views.ProductOrderList.as_view(), name='productOrder'),
    path('order/popup/<int:pk>', views.ProductOrderPopup.as_view(), name='productOrderPopup'),
    path('order/finish', views.ProductOrderFinish.as_view(), name='productOrderFinish'),
    path('recall/<int:pk>', views.ProductRecall.as_view(), name='productRecall'),
    path('productReport', views.ProductReport.as_view(), name='productReport'),
    path('productOEMReg', views.ProductOEMReg.as_view(), name='productOEMReg'),
    path('productOEMList', views.ProductOEMList.as_view(), name='productOEMList'),
    path('ProductUnitPricesList', views.ProductUnitPricesList.as_view(), name='productUnitPricesList'),
    path('setProductMatchList', views.SetProductMatchList.as_view(), name='setProductMatchList'),
    path('autoPackingList', views.AutoPackingList.as_view(), name='autoPackingList'),
    path('productCodeList', views.ProductCodeList.as_view(), name='productCodeList'),
]
