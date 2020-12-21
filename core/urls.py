from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.LocationReg.as_view(), name='locationReg'),
    path('list', views.LocationList.as_view(), name='locationList'),
    path('audit', views.Audit.as_view(), name='audit'),
]
