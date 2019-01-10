from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('ProductUnitPriceMigrate', views.ProductUnitPriceMigrate.as_view()),
    path('LocationMigrate', views.LocationMigrate.as_view()),
    path('ProductCodeMigrate', views.ProductCodeMigrate.as_view()),
    path('SetProductCodeMigrate', views.SetProductCodeMigrate.as_view()),
    path('SetProductMatchMigrate', views.SetProductMatchMigrate.as_view()),
    path('EggCodeMigrate', views.EggCodeMigrate.as_view()),
    path('PackingCodeMigrate', views.PackingCodeMigrate.as_view()),
]
