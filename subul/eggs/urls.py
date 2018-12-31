from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.EggReg.as_view(), name='eggsReg'),
    path('list', views.EggList.as_view(), name='eggsList'),
    path('release', views.EggRelease.as_view(), name='eggsRelease'),
]
