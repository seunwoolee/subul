from django.urls import path
from .views import ProductsAPIView, ProductUpdate, ProductEggUpdate, OrderProductUnitPrice, OrderSetProductMatch, \
    OrderSetProductCode, ProductCodes, OrdersAPIView, OrderUpdate, ProductAdminsAPIView, ReleasesAPIView, ReleaseUpdate, \
    ProductMasterUpdate, EggsAPIView, EggsListAPIView, EggsUpdate, EggsReportAPIView, PackingListAPIView, PackingUpdate, \
    PackingAPIView, PackingReportAPIView, ProductSummaryAPIView

urlpatterns = [
    # 생산쪽 API
    path('product/', ProductsAPIView.as_view()),
    path('productSummary/', ProductSummaryAPIView.as_view()),
    path('productMaster/<slug:ymd>', ProductMasterUpdate.as_view()),
    path('product/<int:pk>', ProductUpdate.as_view()),
    path('productEgg/<int:pk>', ProductEggUpdate.as_view()),
    path('productCodes/<slug:code>', ProductCodes.as_view()),
    # 주문쪽 API
    path('order/', OrdersAPIView.as_view()),
    path('order/<int:pk>', OrderUpdate.as_view()),
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
    # 포장재쪽 API
    path('packing/', PackingAPIView.as_view()),
    path('packing/<int:pk>', PackingUpdate.as_view()),
    path('packingList/', PackingListAPIView.as_view()),
    path('packingReport/', PackingReportAPIView.as_view()),
]