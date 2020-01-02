import json
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.db.models import Sum, F, ExpressionWrapper, Q, Count, DecimalField, Manager
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views import View
from core.models import Location
from eventlog.models import LogginMixin
from order.models import Order
from packing.models import AutoPacking
from release.forms import ReleaseForm, ReleaseLocationForm, CarForm
from release.services import CarServices
from .models import Release, OrderList, Car, Pallet
from product.models import ProductCode, SetProductCode, Product, ProductAdmin
from django.core.serializers.json import DjangoJSONEncoder
from .utils import render_to_pdf


class GeneratePDF(View):

    def get(self, request, *args, **kwargs):
        ymd = request.GET['ymd']
        yyyymmdd = "{}/{}/{}".format(ymd[0:4], ymd[4:6], ymd[6:])
        releaseLocationCode = request.GET['releaseLocationCode']
        moneyMark = request.GET['moneyMark']
        location = Location.objects.get(code=releaseLocationCode)
        releases = Release.objects.filter(ymd=ymd).filter(releaseLocationCode=location) \
            .filter(type__in=['판매', '샘플', '증정']) \
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
            filename = "invoice.pdf"
            content = "inline; filename=%s" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename=%s" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


class ReleaseList(LoginRequiredMixin, View):
    def get(self, request):
        form = ReleaseForm(auto_id=False)
        return render(request, 'release/releaseList.html', {'form': form})


class ReleaseReg(LogginMixin, LoginRequiredMixin, View):

    def post(self, request):
        data = request.POST.dict()
        productCode = ProductCode.objects.get(code=data['productCode'])
        releaseLocation = Location.objects.get(code=data['location'])
        releaseStoreLocation = Location.objects.get(code=data['storedLocationCode'])
        releaseOrder = int(data['releaseOrder'])
        setProductCode = request.POST.get('setProductCode', None)
        specialTag = request.POST.get('specialTag', '')
        totalPrice = int(Decimal(data['price']) * int(data['count']))

        if setProductCode:  # 세트 상품 존재 시 부가세 0원
            releaseVat = 0
        else:
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
        self.log(
            user=request.user,
            action="출고등록",
            obj=release,
            extra=data
        )
        return HttpResponse(status=200)

    def get(self, request):
        releaseForm = ReleaseForm()
        releaseLocationForm = ReleaseLocationForm()
        return render(request, 'release/releaseReg.html', {'releaseForm': releaseForm,
                                                           'releaseLocationForm': releaseLocationForm})


class ReleaseAdjustment(LogginMixin, View):  # 재고조정, 미출고품, 반품
    def post(self, request):
        data = request.POST.dict()
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
        self.log(
            user=request.user,
            action="출고리콜",
            obj=release,
            extra=data
        )
        return HttpResponse(status=200)


class ReleaseOrderList(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'release/releaseOrder.html')


class ReleaseOrder(View):

    def get(self, request):
        self.result = {}
        location_id = request.GET.get('location_id', None)
        pallet_id = request.GET.get('pallet_id', None)
        ymd = request.GET.get('ymd', None)
        type = request.GET.get('type', None)
        if type == 'unloaded':
            orders = self.get_unloaded_query(location_id, ymd)
        else:
            orders = self.get_loaded_query(pallet_id, ymd)
        self.get_list(orders, pallet_id)
        return JsonResponse(self.result)

    def get_unloaded_query(self, location_id, ymd):
        location = Location.objects.get(id=location_id)
        orders = OrderList.objects.filter(Q(ymd=ymd),
                                          Q(location=location),
                                          Q(pallet=None))\
            .annotate(types=F('productCode__type')) \
            .annotate(amount_types=F('productCode__amount_kg')) \
            .annotate(amount=ExpressionWrapper(F('count') * F('productCode__amount_kg'), output_field=DecimalField())) \
            .order_by('id')
        return orders

    def get_loaded_query(self, pallet_id, ymd):
        pallet = Pallet.objects.get(id=pallet_id)
        orders = OrderList.objects.filter(Q(ymd=ymd), Q(pallet=pallet))\
            .annotate(types=F('productCode__type')) \
            .annotate(amount_types=F('productCode__amount_kg')) \
            .annotate(amount=ExpressionWrapper(F('count') * F('productCode__amount_kg'), output_field=DecimalField())) \
        .order_by('id')
        return orders

    def get_list(self, orders, pallet_id):
        self.result['list'] = render_to_string('release/partial_releaseOrder_list.html',
                                               {'orders': orders, 'pallet_id': pallet_id})

    def post(self, request):
        ymd = self.request.POST.get('ymd')
        orders = self.create_order_lists(ymd)

        for order in orders:
            self.calculate_box_with_create(order)

        return HttpResponse(status=200)

    def create_order_lists(self, ymd):
        orders = Order.objects.values('orderLocationCode', 'orderLocationName', 'ymd', 'code', 'codeName').annotate(totalCount=Sum('count')).filter(ymd=ymd)
        for order in orders:
            existing_order = OrderList.objects.filter(Q(ymd=ymd),
                                                      Q(code=order['code']),
                                                      Q(location__id=order['orderLocationCode']),
                                                      Q(count=order['totalCount'])).first()
            if existing_order:
                orders = orders.exclude(Q(ymd=order['ymd']), Q(code=order['code']), Q(orderLocationCode=order['orderLocationCode']))
        return orders

    def calculate_box_with_create(self, order):
        big_box = AutoPacking.objects.filter(productCode=ProductCode.objects.get(code=order['code'])).filter(packingCode__type='외포장재').first()

        if big_box:
            order['box'], order['ea'] = divmod(order['totalCount'], big_box.count)
        else:
            order['box'], order['ea'] = 0, 0

        order = self.create_order_dict_format(order)
        OrderList(**order).save()

    def create_order_dict_format(self, order):
        order['location'] = Location.objects.get(id=order['orderLocationCode'])
        order['productCode'] = ProductCode.objects.get(code=order['code'])
        order['locationCodeName'] = order['orderLocationName']
        order['count'] = order['totalCount']
        del order['orderLocationCode']
        del order['orderLocationName']
        del order['totalCount']
        return order


class ReleaseOrderCar(View):
    def get(self, request):
        self.result = {}
        car_id = request.GET.get('car_id', None)
        pallet_id = int(request.GET.get('pallet_id', '0'))
        ymd = request.GET.get('ymd', None)
        pallets = Pallet.objects.filter(car__id=car_id).annotate(
            counts=Count('order_list', filter=Q(order_list__ymd=ymd))
        ).order_by('car__car_number', 'seq')
        self.get_list(pallets, pallet_id)
        return JsonResponse(self.result)

    def get_list(self, pallets, pallet_id):
        self.result['list'] = render_to_string('release/partial_releaseOrder_pallet.html'
                                               , {'pallets': pallets, 'selected_pallet_id': pallet_id})

    def post(self, request):
        pallet_id = request.POST.get('pallet_id')
        order_list_ids = request.POST.get('order_list_id').split(',')
        self.clear_current_pallet(pallet_id)
        if order_list_ids[0]:
            self.load_order_to_pallet(pallet_id, order_list_ids)

        return HttpResponse(status=200)

    def clear_current_pallet(self, pallet_id):
        for orderList in OrderList.objects.filter(pallet_id=pallet_id):
            orderList.pallet = None
            orderList.save()

    def load_order_to_pallet(self, pallet_id, order_list_ids):

        for orderList in OrderList.objects.filter(id__in=order_list_ids):
            orderList.pallet_id = pallet_id
            orderList.save()


class CarCodeReg(View):
    def get(self, request):
        carForm = CarForm()
        return render(request, 'code/carReg.html', {'form': carForm})

    def post(self, request):
        services = CarServices()
        data: dict = request.POST.copy()
        pallet_count: int = data['pallet_count']
        form: CarForm = CarForm(data)
        if form.is_valid():
            car = form.save()
            services.save_pallet(pallet_count, car)
        else:
            messages.error(request, '저장 실패(중복된 차량 넘버)')

        return redirect('carCodeReg')


class CarCodeList(View):
    def get(self, request):
        form = CarForm()
        return render(request, 'code/carList.html', {'form': form})


class ReleaseOrderPrint(View):
    def get(self, request):
        car_id = request.GET.get('car_id', None)
        pallet_id = request.GET.get('pallet_id', None)
        ymd = request.GET.get('ymd', None)

        # orderList: Manager = OrderList.objects.annotate(pallet_seq=F('pallet__seq'))\
        #     .filter(Q(ymd=ymd), Q(pallet__car_id=car_id), Q(pallet_id=pallet_id)).values()

        orderList: Manager = OrderList.objects.annotate(pallet_seq=F('pallet__seq'))\
            .filter(Q(ymd=ymd), Q(pallet__car_id=car_id)).order_by('pallet__seq', 'locationCodeName').values()
        address_categorys = OrderList.objects.filter(Q(ymd=ymd), Q(pallet__car_id=car_id))\
            .values(address_category=F('location__location_address_category')).distinct()

        if not len(address_categorys) == 1:
            return render(request, 'release/releasetReport.html', {'rows': 0,
                                                                   'address_category': 0,
                                                                   'title': 0})

        title = ymd[4:6] + '월' + ymd[6:8] + '일' + ' 출하지시서'
        rows = json.dumps(list(orderList))
        return render(request, 'release/releasetReport.html',
                      {'rows': rows,
                       'address_category': address_categorys[0]['address_category'],
                       'title': title})

