from django.urls import path, include

from labor.views import SiteEggOrder, SiteProductOrder, Nav
from subul import views

urlpatterns = [
    path('egg', SiteEggOrder.as_view(), name='labor_egg'),
    path('egg/<int:pk>', SiteEggOrder.as_view(), name='labor_egg_post'),
    path('product', SiteProductOrder.as_view(), name='labor_product'),
    path('nav', Nav.as_view(), name='labor_nav'),
]
