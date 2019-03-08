from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F, ExpressionWrapper, FloatField, IntegerField
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from core.models import Location
from order.models import Order
from release.forms import ReleaseForm, ReleaseLocationForm
from .models import Release
from product.models import ProductCode, SetProductCode, Product, ProductAdmin

from .utils import render_to_pdf
import datetime


class GeneratePDF(View):

    def get(self, request, *args, **kwargs):
        ymd = request.GET['ymd']
        yyyymmdd = "{}/{}/{}".format(ymd[0:4], ymd[4:6], ymd[6:])
        releaseLocationCode = request.GET['releaseLocationCode']
        moneyMark = request.GET['moneyMark']
        location = Location.objects.get(code=releaseLocationCode)
        releases = Release.objects.filter(ymd=ymd).filter(releaseLocationCode=location) \
            .filter(type__in=['판매', '샘플', '증정'])\
            .values('code', 'codeName', 'price', 'specialTag', 'releaseVat') \
            .annotate(totalCount=Sum('count')) \
            .annotate(totalPrice=F('price')) \
            .annotate(supplyPrice=F('totalPrice') - F('releaseVat'))
        sumTotalCount = releases.aggregate(sumTotalCount=Sum('totalCount'))
        sumSupplyPrice = releases.aggregate(sumSupplyPrice=Sum('supplyPrice'))
        sumVat = releases.aggregate(sumVat=Sum('releaseVat'))
        sumTotal = sumSupplyPrice['sumSupplyPrice'] + sumVat['sumVat']
        sumData = {'sumTotalCount': sumTotalCount['sumTotalCount'],
                   'sumSupplyPrice': sumSupplyPrice['sumSupplyPrice'],
                   'sumVat': sumVat['sumVat'],
                   'sumTotal': sumTotal,
                   'moneyMark': moneyMark}
        context_dict = {
            "yyyymmdd": yyyymmdd,
            "orders": releases,
            "sumData": sumData,
            "location": location,
        }
        pdf = render_to_pdf('invoice/출고거래명세표.html', context_dict)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "거래명세표_{}_{}.pdf".format(yyyymmdd, location.codeName)
            content = "inline; filename={}".format(filename).encode('utf-8')
            download = request.GET.get("download")
            if download:
                content = "attachment; filename={}".format(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


class ReleaseList(LoginRequiredMixin, View):
    def get(self, request):
        form = ReleaseForm(auto_id=False)
        return render(request, 'release/releaseList.html', {'form': form})


class ReleaseReg(LoginRequiredMixin, View):

    def post(self, request):
        data = request.POST.dict()
        productCode = ProductCode.objects.get(code=data['productCode'])
        releaseLocation = Location.objects.get(code=data['location'])
        releaseStoreLocation = Location.objects.get(code=data['storedLocationCode'])
        releaseOrder = int(data['releaseOrder'])
        setProductCode = request.POST.get('setProductCode', None)
        specialTag = request.POST.get('specialTag', '')
        totalPrice = int(Decimal(data['price']) * int(data['count']))
        releaseVat = round(totalPrice - (totalPrice / 1.1)) if productCode.vat else 0  # vat 계산
        release = Release.objects.create(
            ymd=data['ymd'],
            productYmd=data['productYmd'],
            code=data['productCode'],
            codeName=productCode.codeName,
            count=data['count'],
            amount=data['amount'],
            amount_kg=data['amount_kg'],
            type=data['type'],
            product_id=Product.objects.get(id=data['productId']),
            memo=data['memo'],
            releaseLocationCode=releaseLocation,
            releaseLocationName=releaseLocation.codeName,
            releaseStoreLocation=releaseStoreLocation,
            price=totalPrice,
            releaseVat=releaseVat,
            specialTag=specialTag
        )

        if releaseOrder:  # 주문 기반 출고
            order = Order.objects.get(id=releaseOrder)
            release.releaseOrder = order
            order.release_id = release
            order.save()

        if setProductCode:  # 세트 상품 존재
            release.releaseSetProductCode = SetProductCode.objects.get(code=setProductCode)

        ProductAdmin.objects.create(
            product_id=Product.objects.get(id=data['productId']),
            count=-int(data['count']),
            amount=-Decimal(data['amount']),
            ymd=data['ymd'],
            location=releaseStoreLocation,
            releaseType=data['type'],
            releaseSeq=release
        )

        if data['type'] == '이동':  # 이동장소에 재고 +
            ProductAdmin.objects.create(
                product_id=Product.objects.get(id=data['productId']),
                count=int(data['count']),
                amount=Decimal(data['amount']),
                ymd=data['ymd'],
                location=releaseLocation,
                releaseType='생성',
                releaseSeq=release
            )

        release.save()
        return HttpResponse(status=200)

    def get(self, request):
        releaseForm = ReleaseForm()
        releaseLocationForm = ReleaseLocationForm()
        return render(request, 'release/releaseReg.html', {'releaseForm': releaseForm,
                                                           'releaseLocationForm': releaseLocationForm})


class ReleaseAdjustment(View): # 재고조정, 미출고품, 반품
    def post(self, request):
        data = request.POST.dict()
        print(data)
        productCode = ProductCode.objects.get(code=data['productCode'])

        if data['type'] != '반품':
            releaseStoreLocation = Location.objects.get(code=data['storedLocationCode'])
            release = Release.objects.create(
                ymd=data['ymd'],
                productYmd=data['productYmd'],
                code=data['productCode'],
                codeName=productCode.codeName,
                count=data['count'],
                amount=data['amount'],
                amount_kg=data['amount_kg'],
                type=data['type'],
                product_id=Product.objects.get(id=data['productId']),
                memo=data['memo'],
                releaseLocationCode=releaseStoreLocation,
                releaseLocationName=releaseStoreLocation.codeName,
                releaseStoreLocation=releaseStoreLocation,
                price=0,
                releaseVat=0
            )

            ProductAdmin.objects.create(
                product_id=Product.objects.get(id=data['productId']),
                count=int(data['count']),
                amount=float(data['amount']),
                ymd=data['ymd'],
                location=releaseStoreLocation,
                releaseType=data['type'],
                releaseSeq=release
            )
        else:
            KCFRESH_CODE = '00301'
            releaseStoreLocation = Location.objects.get(code=KCFRESH_CODE)
            releaseLocation = Location.objects.get(code=data['storedLocationCode'])
            releaseVat = round(float(data['price']) - (float(data['price']) / 1.1)) if productCode.vat else 0  # vat 계산
            release = Release.objects.create(
                ymd=data['ymd'],
                productYmd=data['productYmd'],
                code=data['productCode'],
                codeName=productCode.codeName,
                count=-int(data['count']),
                amount=-float(data['amount']),
                amount_kg=float(data['amount_kg']),
                type=data['type'],
                product_id=Product.objects.get(id=data['productId']),
                memo=data['memo'],
                releaseLocationCode=releaseLocation,
                releaseLocationName=releaseLocation.codeName,
                releaseStoreLocation=releaseStoreLocation,
                price=-int(data['price']),
                releaseVat=-releaseVat
            )

            ProductAdmin.objects.create(
                product_id=Product.objects.get(id=data['productId']),
                count=int(data['count']),
                amount=float(data['amount']),
                ymd=data['ymd'],
                location=releaseLocation,
                releaseType=data['type'],
                releaseSeq=release
            )

        release.save()
        return HttpResponse(status=200)
