from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.EggReg.as_view(), name='eggsReg'),
    path('list', views.EggList.as_view(), name='eggsList'),
    path('release', views.EggRelease.as_view(), name='eggsRelease'),
    path('calculateAmount', views.EggCalculateAmount.as_view(), name='eggsRelease'),
    path('pricePerEa', views.EggPricePerEa.as_view(), name='pricePerEa'),
    path('pdf', views.GeneratePDF.as_view()),
    path('eggsReport', views.EggReport.as_view(), name='eggsReport'),
]
