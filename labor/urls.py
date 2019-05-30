from django.urls import path, include

from labor.views import SiteList
from subul import views

urlpatterns = [
    path('egg', SiteList.as_view(), name='labor_egg'),
    path('egg/<int:pk>', SiteList.as_view(), name='labor_egg_post'),
]
