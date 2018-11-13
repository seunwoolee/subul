from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ReleaseReg.as_view(), name='releaseReg'),
    path('list', views.ReleaseList.as_view(), name='releaseList'),
]