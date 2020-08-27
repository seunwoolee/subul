from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.OrderReg.as_view(),name='orderReg'),
    path('ex',views.OrderRegEx.as_view(),name='orderRegEx'),
    path('list',views.OrderList.as_view(),name='orderList'),
    path('listEx',views.OrderListEx.as_view(),name='orderListEx'),
    path('pdf', views.GeneratePDF.as_view()),
    path('pdf_selected', views.GeneratePDFSelected.as_view()),
]
