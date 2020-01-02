from django.urls import path
from . import views


urlpatterns = [
    path('', views.ReleaseReg.as_view(), name='releaseReg'),
    path('adjustment', views.ReleaseAdjustment.as_view(), name='releaseAdjustment'),
    path('list', views.ReleaseList.as_view(), name='releaseList'),
    path('order', views.ReleaseOrderList.as_view(), name='releaseOrder'),
    path('pdf', views.GeneratePDF.as_view()),
    path('releaseOrder', views.ReleaseOrder.as_view()),
    path('releaseOrderPrint', views.ReleaseOrderPrint.as_view()),
    path('releaseOrderCar', views.ReleaseOrderCar.as_view()),
    path('carCodeReg', views.CarCodeReg.as_view(), name='carCodeReg'),
    path('carCodeList', views.CarCodeList.as_view(), name='carCodeList'),
]
