from django.conf.urls import url
from django.urls import path, include

# from django_select2.forms import Select2WidgetForm
from . import views

urlpatterns = [
    path('',views.ProductView.as_view(),name='home'),
]