from django.urls import path

from .views import ProductsAPIView, ProductUpdate, ProductEggUpdate

urlpatterns = [
    path('product/', ProductsAPIView.as_view()),
    path('product/<int:pk>', ProductUpdate.as_view()),
    path('productEgg/<int:pk>', ProductEggUpdate.as_view()),
]