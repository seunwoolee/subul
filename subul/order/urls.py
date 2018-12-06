from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.OrderReg.as_view(),name='orderReg'),
    path('list',views.OrderList.as_view(),name='orderList'),

    # PDF 테스트
    path('pdf', views.GeneratePDF.as_view()),
]