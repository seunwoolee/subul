from django.conf.urls import url
from django.urls import path, include

# from django_select2.forms import Select2WidgetForm
from . import views
from .views import TemplateFormView
from .forms import Select2WidgetForm

urlpatterns = [
    path('',views.ProductView.as_view(),name='home'),
    url(r'^select2_widget/$',
        TemplateFormView.as_view(), name='select2_widget'),
    # url(r'^select2/', include('django_select2.urls')),
]