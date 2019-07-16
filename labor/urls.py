from django.urls import path, include

from labor.views import SiteEggOrder, SiteProductOrder, PWA
from subul import views

urlpatterns = [
    path('egg', SiteEggOrder.as_view(), name='labor_egg'),
    path('egg/<int:pk>', SiteEggOrder.as_view(), name='labor_egg_post'),
    path('product', SiteProductOrder.as_view(), name='labor_product'),
    path('pwa', PWA.as_view(), name='labor_product'),
]
