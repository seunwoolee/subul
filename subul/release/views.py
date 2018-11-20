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
            data = request.POST.dict()
            print(data)
            productCode = ProductCode.objects.get(code=data['productCode'])
            releaseVat = round(int(data['price']) - (int(data['price']) / 1.1)) if productCode.vat else 0 # vat 계산
            releaseLocation = Location.objects.get(code=data['location'])
            releaseStoreLocation = Location.objects.get(code=data['storedLocationCode'])
            releaseOrder = int(data['releaseOrder'])
            setProductCode = request.POST.get('setProductCode',None)
            specialTag = request.POST.get('specialTag', '일반')

            if data['count'] and data['amount']:
                totalPrice = int(data['price']) * int(data['count'])
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

                if releaseOrder: #주문 기반 출고
                    order = Order.objects.get(id=releaseOrder)
                    release.releaseOrder = order
                    order.release_id = release
                    order.save()

                if setProductCode: # 세트 상품 존재
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

                if data['type'] == '이동': # 이동장소에 재고 +
                    ProductAdmin.objects.create(
                        product_id=Product.objects.get(id=data['productId']),
                        count=int(data['count']),
                        amount=float(data['amount']),
                        ymd=data['productYmd'],
                        location=releaseLocation,
                        releaseType='생성',
                        # releaseSeq=release
                    )

                release.save()

            return HttpResponse(status=200)


        def get(self, request):
            releaseForm = ReleaseForm()
            releaseLocationForm = ReleaseLocationForm()
            return render(request, 'release/releaseReg.html', {'releaseForm': releaseForm,
                                                                   'releaseLocationForm': releaseLocationForm})


class ReleaseAdjustment(View):
        def post(self, request):
            data = request.POST.dict()
            productCode = ProductCode.objects.get(code=data['productCode'])
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
                ymd=data['productYmd'],
                location=releaseStoreLocation,
                releaseType=data['type'],
                releaseSeq=release
            )

            release.save()
            return HttpResponse(status=200)