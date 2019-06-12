from django.contrib import admin
from django.urls import path, include

from subul import views

urlpatterns = [
    path('accounts/', include('users.urls')),
    path('product/', include('product.urls')),
    path('order/', include('order.urls')),
    path('release/', include('release.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('eggs/', include('eggs.urls')),
    path('packing/', include('packing.urls')),
    path('core/', include('core.urls')),
    path('labor/', include('labor.urls')),
    path('', views.MainList.as_view(), name='index'),
]
