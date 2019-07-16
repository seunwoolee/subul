from django.urls import path
from .views import ProductsAPIView, ProductUpdate, ProductEggUpdate, OrderProductUnitPrice, OrderSetProductMatch, \
    OrderSetProductCode, ProductCodes, OrdersAPIView, OrderUpdate, ProductAdminsAPIView, ReleasesAPIView, ReleaseUpdate, \
    EggsAPIView, EggsListAPIView, EggsUpdate, EggsReportAPIView, PackingListAPIView, PackingUpdate, \
    PackingAPIView, PackingReportAPIView, ProductSummaryAPIView, ProductOEMsAPIView, ProductOEMUpdate, \
    ProductUnitPricesAPIView, ProductUnitPricesUpdate, SetProductMatchsAPIView, SetProductMatchsUpdate, \
    LocationsAPIView, LocationUpdate, AutoPackingAPIView, AutoPackingUpdate, OrderLocation, EggOrderListAPIView, \
    EggOrderUpdate, ProductOrderListAPIView, ProductOrderUpdate, ProductOrderPackingUpdate, ProductCodeByPk

urlpatterns = [
    # 생산쪽 API
    path('product/', ProductsAPIView.as_view()),
    path('productSummary/', ProductSummaryAPIView.as_view()),
    path('product/<int:pk>', ProductUpdate.as_view()),
    path('productEgg/<int:pk>', ProductEggUpdate.as_view()),
    path('productCodes/<slug:code>', ProductCodes.as_view()),
    path('productCodeByPk/<int:pk>', ProductCodeByPk.as_view()),
    path('productOrder/', ProductOrderListAPIView.as_view()),
    path('productOrder/<int:pk>', ProductOrderUpdate.as_view()),
    path('productOrderPacking/<int:pk>', ProductOrderPackingUpdate.as_view()),
    # OEM쪽 API
    path('productOEM/', ProductOEMsAPIView.as_view()),
    path('productOEM/<int:pk>', ProductOEMUpdate.as_view()),
    # 주문쪽 API
    path('order/', OrdersAPIView.as_view()),
    path('order/<int:pk>', OrderUpdate.as_view()),
    path('orderLocation/', OrderLocation.as_view()),
    path('OrderProductUnitPrice/<slug:code>', OrderProductUnitPrice.as_view()),
    path('OrderSetProductCode/<slug:code>', OrderSetProductCode.as_view()),
    path('OrderSetProductMatch/<slug:code>', OrderSetProductMatch.as_view()),
    # 출고쪽 API
    path('productAdmin/', ProductAdminsAPIView.as_view()),
    path('release/', ReleasesAPIView.as_view()),
    path('release/<int:pk>', ReleaseUpdate.as_view()),
    # 원란쪽 API
    path('eggs/', EggsAPIView.as_view()),
    path('eggs/<int:pk>', EggsUpdate.as_view()),
    path('eggsList/', EggsListAPIView.as_view()),
    path('eggsReport/', EggsReportAPIView.as_view()),
    path('eggsOrderList/', EggOrderListAPIView.as_view()),
    path('eggsOrder/<int:pk>', EggOrderUpdate.as_view()),
    # 포장재쪽 API
    path('packing/', PackingAPIView.as_view()),
    path('packing/<int:pk>', PackingUpdate.as_view()),
    path('packingList/', PackingListAPIView.as_view()),
    path('packingReport/', PackingReportAPIView.as_view()),
    # 코드쪽 API
    path('location/', LocationsAPIView.as_view()),
    path('location/<int:pk>', LocationUpdate.as_view()),
    path('productUnitPrices/', ProductUnitPricesAPIView.as_view()),
    path('productUnitPrices/<int:pk>', ProductUnitPricesUpdate.as_view()),
    path('autoPacking/', AutoPackingAPIView.as_view()),
    path('autoPacking/<int:pk>', AutoPackingUpdate.as_view()),
    path('setProductMatch/', SetProductMatchsAPIView.as_view()),
    path('setProductMatch/<int:pk>', SetProductMatchsUpdate.as_view()),
]
