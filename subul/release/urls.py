from django.conf.urls import url
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.ReleaseReg.as_view(), name='releaseReg'),
    path('adjustment', views.ReleaseAdjustment.as_view(), name='releaseAdjustment'),
    path('list', views.ReleaseList.as_view(), name='releaseList'),

    # PDF 테스트
    path('pdf', views.GeneratePDF.as_view()),
]