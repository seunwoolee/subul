from django.urls import path

from labor.views import SiteEggOrder, SiteProductOrder, Nav, SiteReleaseOrder

urlpatterns = [
    path('egg', SiteEggOrder.as_view(), name='labor_egg'),
    path('egg/<int:pk>', SiteEggOrder.as_view(), name='labor_egg_post'),
    path('product', SiteProductOrder.as_view(), name='labor_product'),
    path('release', SiteReleaseOrder.as_view(), name='labor_release'),
    path('nav', Nav.as_view(), name='labor_nav'),
]
