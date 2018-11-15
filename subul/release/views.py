from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from core.models import Location
from order.forms import OrderFormSet
from order.models import Order
from release.forms import ReleaseForm, ReleaseLocationForm
from .models import Release
from product.models import ProductCode, SetProductCode, Product, ProductAdmin


class ReleaseList(View):
    def get(self, request):
        return render(request, 'release/releaseList.html')


class ReleaseReg(View):

        def post(self, request):
            data = request.POST.dict() # productCode, locatoinCode, type, location, ymd, amount, count, price, memo
            productCode = ProductCode.objects.get(code=data['productCode'])
            releaseVat = round(data['price'] - (data['price'] / 1.1)) if productCode.vat else 0 # vat 계산
            releaseLocation = Location.objects.get(code=data['location'])
            releaseStoreLocation = Location.objects.get(code=data['storedLocationCode'])
            totalPrice = int(data['price']) * int(data['count'])
            releaseOrder = int(data['releaseOrder'])
            setProductCode = request.POST.get('setProductCode',None)

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
                releaseVat=releaseVat
            )

            if releaseOrder: #출고 매뉴얼은 0으로 넘김
                order = Order.objects.get(id=releaseOrder)
                release.releaseOrder = order
                order.release_id = release
                order.save()

            if setProductCode: # 세트 상품이 있으면
                release.releaseSetProductCode = SetProductCode.objects.get(code=setProductCode)

            ProductAdmin.objects.create(
                product_id=Product.objects.get(id=data['productId']),
                count=-int(data['count']),
                amount=-float(data['amount']),
                ymd=data['productYmd'],
                location=releaseStoreLocation,
                releaseType=data['type'],
                releaseSeq=release
            )
            release.save()
            return HttpResponse(status=200)

        def get(self, request):
            releaseForm = ReleaseForm()
            releaseLocationForm = ReleaseLocationForm()
            return render(request, 'release/releaseReg.html', {'releaseForm': releaseForm,
                                                                   'releaseLocationForm': releaseLocationForm})
