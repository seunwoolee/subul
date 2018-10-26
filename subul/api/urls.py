from django.urls import path
from .views import ProductsAPIView, ProductUpdate, ProductEggUpdate, OrderProductUnitPrice, OrderSetProductMatch, \
    OrderSetProductCode, ProductCodes

urlpatterns = [
    # 생산쪽 API
    path('product/', ProductsAPIView.as_view()),
    path('product/<int:pk>', ProductUpdate.as_view()),
    path('productEgg/<int:pk>', ProductEggUpdate.as_view()),
    path('productCodes/<slug:code>', ProductCodes.as_view()),
    # 주문쪽 API
    path('OrderProductUnitPrice/<slug:code>', OrderProductUnitPrice.as_view()),
    path('OrderSetProductCode/<slug:code>', OrderSetProductCode.as_view()),
    path('OrderSetProductMatch/<slug:code>', OrderSetProductMatch.as_view()),
]