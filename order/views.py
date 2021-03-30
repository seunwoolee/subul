import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from model_utils.managers import QueryManager
from openpyxl.worksheet import worksheet
from openpyxl.worksheet.worksheet import Worksheet

from core.models import Location, OrderTime
from eggs.models import Egg
from eventlog.models import LogginMixin
from order.forms import OrderFormSet, OrderForm, OrderFormExSet
from order.models import Order, ABS
from product.models import ProductCode, SetProductCode, ProductUnitPrice
from django.db.models import Sum, F, ExpressionWrapper, FloatField, IntegerField, Func, Value, CharField, Q, QuerySet
from core.utils import render_to_pdf
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from openpyxl import load_workbook, Workbook

from users.models import CustomUser


class Round(Func):
    function = 'ROUND'


def create_pdf_orders(ymd: str, location: Location):
    return Order.objects.filter(Q(ymd=ymd), Q(orderLocationCode=location)) \
        .values('code', 'codeName', 'price', 'specialTag', 'memo') \
        .annotate(totalCount=Sum('count')) \
        .annotate(pricePerEa=F('price')) \
        .annotate(totalPrice=ExpressionWrapper(F('totalCount') * F('price'), output_field=IntegerField())) \
        .annotate(vat=ExpressionWrapper(F('productCode__vat') * 0.01 + 1, output_field=FloatField())) \
        .annotate(supplyPrice=ExpressionWrapper(Round(F('totalPrice') / F('vat')), output_field=IntegerField())) \
        .annotate(vatPrice=F('totalPrice') - F('supplyPrice'))


def create_pdf_selected_orders(ids: list):
    return Order.objects.filter(Q(id__in=ids)) \
        .values('code', 'codeName', 'price', 'specialTag', 'memo') \
        .annotate(totalCount=Sum('count')) \
        .annotate(pricePerEa=F('price')) \
        .annotate(totalPrice=ExpressionWrapper(F('totalCount') * F('price'), output_field=IntegerField())) \
        .annotate(vat=ExpressionWrapper(F('productCode__vat') * 0.01 + 1, output_field=FloatField())) \
        .annotate(supplyPrice=ExpressionWrapper(Round(F('totalPrice') / F('vat')), output_field=IntegerField())) \
        .annotate(vatPrice=F('totalPrice') - F('supplyPrice'))


def create_pdf_sum(orders: QueryManager):
    sumTotalCount = orders.aggregate(sumTotalCount=Sum('totalCount'))
    sumSupplyPrice = orders.aggregate(sumSupplyPrice=Sum('supplyPrice'))
    sumVat = orders.aggregate(sumVat=Sum('vatPrice'))
    sumTotal = sumSupplyPrice['sumSupplyPrice'] + sumVat['sumVat']
    return sumTotalCount, sumSupplyPrice, sumVat, sumTotal


class GeneratePDF(View):

    def get(self, request, *args, **kwargs):
        ymd = request.GET['ymd']
        yyyymmdd = "{}/{}/{}".format(ymd[0:4], ymd[4:6], ymd[6:])
        orderLocationCode = request.GET['orderLocationCode']
        moneyMark = request.GET['moneyMark']
        location = Location.objects.get(code=orderLocationCode)
        egg_location = Location.objects.filter(codeName=location.codeName).filter(type='07').first()
        orders = create_pdf_orders(ymd, location)

        if egg_location:
            eggs = Egg.objects.filter(ymd=ymd).filter(locationCode=egg_location) \
                .values('code', 'codeName', 'price') \
                .annotate(specialTag=Value('', CharField())) \
                .annotate(memo=F('memo')) \
                .annotate(totalCount=ABS(Sum('count'))) \
                .annotate(
                pricePerEa=ExpressionWrapper(Round(F('price') / F('totalCount')), output_field=IntegerField())) \
                .annotate(totalPrice=F('price')) \
                .annotate(vat=Value(1, IntegerField())) \
                .annotate(supplyPrice=ExpressionWrapper(Round(F('totalPrice') / F('vat')), output_field=IntegerField())) \
                .annotate(vatPrice=F('totalPrice') - F('supplyPrice'))
            orders = orders.union(eggs)

        sumTotalCount, sumSupplyPrice, sumVat, sumTotal = create_pdf_sum(orders)
        sumData = {'sumTotalCount': sumTotalCount['sumTotalCount'],
                   'sumSupplyPrice': sumSupplyPrice['sumSupplyPrice'],
                   'sumVat': sumVat['sumVat'],
                   'sumTotal': sumTotal,
                   'moneyMark': moneyMark}
        context_dict = {
            "yyyymmdd": yyyymmdd,
            "orders": orders,
            "sumData": sumData,
            "location": location,
        }
        pdf = render_to_pdf('invoice/주문거래명세표.html', context_dict)
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


class GeneratePDFSelected(View):
    def get(self, request, *args, **kwargs):
        ymd: str = request.GET['ymd']
        selectedRows: str = request.GET['selectedRows']
        orderLocationCode: str = request.GET['orderLocationCode']
        location = Location.objects.get(code=orderLocationCode)
        moneyMark: str = request.GET['moneyMark']
        yyyymmdd = "{}/{}/{}".format(ymd[0:4], ymd[4:6], ymd[6:])
        orders = create_pdf_selected_orders(selectedRows.split(','))
        sumTotalCount, sumSupplyPrice, sumVat, sumTotal = create_pdf_sum(orders)
        sumData = {'sumTotalCount': sumTotalCount['sumTotalCount'],
                   'sumSupplyPrice': sumSupplyPrice['sumSupplyPrice'],
                   'sumVat': sumVat['sumVat'],
                   'sumTotal': sumTotal,
                   'moneyMark': moneyMark}
        context_dict = {
            "yyyymmdd": yyyymmdd,
            "orders": orders,
            "sumData": sumData,
            "location": location,
        }
        pdf = render_to_pdf('invoice/주문거래명세표.html', context_dict)
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


class OrderList(LoginRequiredMixin, View):

    def get(self, request):
        form = OrderForm()
        return render(request, 'order/orderList.html', {'form': form})


class OrderReg(LogginMixin, LoginRequiredMixin, View):

    def post(self, request):
        formset = OrderFormSet(request.POST)
        self.log(
            user=request.user,
            action="주문등록",
            obj=Order.objects.first(),
            extra=request.POST
        )

        if formset.is_valid():
            for form in formset:
                setProduct = None
                ymd = form.cleaned_data.get('ymd')
                code = form.cleaned_data.get('product')
                productCode = ProductCode.objects.get(code=code)
                codeName = productCode.codeName
                count = form.cleaned_data.get('count')
                amount = form.cleaned_data.get('amount')
                amount_kg = form.cleaned_data.get('amount_kg')
                memo = form.cleaned_data.get('memo')
                price = form.cleaned_data.get('price')
                type = form.cleaned_data.get('type')
                location = Location.objects.get(code=form.cleaned_data.get('location'))
                specialTag = form.cleaned_data.get('specialTag')

                if form.cleaned_data.get('package'):
                    setProduct = SetProductCode.objects.get(code=form.cleaned_data.get('package'))

                order = Order.objects.create(
                    ymd=ymd,
                    code=code,
                    codeName=codeName,
                    amount=amount,
                    count=count,
                    amount_kg=amount_kg,
                    price=price,
                    memo=memo,
                    orderLocationCode=location,
                    orderLocationName=location.codeName,
                    type=type,
                    specialTag=specialTag,
                    productCode=productCode,
                )

                if setProduct:
                    order.setProduct = setProduct
                    order.save()

        else:
            self.log(
                user=request.user,
                action="주문등록에러",
                obj=Order.objects.first(),
                extra=formset.errors[0]
            )
        return redirect('orderReg')

    def get(self, request):
        orderForm = OrderFormSet(request.GET or None)
        return render(request, 'order/orderReg.html', {'orderForm': orderForm})


class OrderRegEx(LogginMixin, LoginRequiredMixin, View):

    def is_valid_order(self, request):
        user: CustomUser = request.user
        now = datetime.datetime.now()
        if user.last_name != '업체':
            return True

        weekday = now.weekday()
        weekday = weekday + 1
        if weekday == 7:
            weekday = 0  # 일요일

        order_time: OrderTime = user.order_time.filter(weekday=weekday).first()
        if not order_time:  # 외부 업체인데 시간이 미정이면 등록못함
            return False

        current_time: int = int(now.strftime('%H%M'))
        start: list = order_time.start.split(':')
        end: list = order_time.end.split(':')

        start: int = int(start[0] + start[1])
        end: int = int(end[0] + end[1])

        if start < current_time < end:
            return True

        return False

    def post(self, request):
        if self.request.user.is_staff:
            return redirect('orderRegEx')

        if not self.is_valid_order(request):
            messages.info(request, '주문 가능한 시간이 아닙니다.')
            return redirect('orderRegEx')

        formset = OrderFormExSet(request.POST)
        self.log(
            user=request.user,
            action="외부주문등록",
            obj=Order.objects.first(),
            extra=request.POST
        )

        if formset.is_valid():
            for form in formset:
                ymd = form.cleaned_data.get('ymd')
                code = form.cleaned_data.get('product')
                productCode = ProductCode.objects.get(code=code)
                codeName = productCode.codeName
                count = form.cleaned_data.get('count')
                amount = form.cleaned_data.get('amount')
                amount_kg = form.cleaned_data.get('amount_kg')
                memo = form.cleaned_data.get('memo')
                price = form.cleaned_data.get('price')
                user: User = request.user

                location = Location.objects.get(code=user.first_name)

                Order.objects.create(
                    ymd=ymd,
                    code=code,
                    codeName=codeName,
                    amount=amount,
                    count=count,
                    amount_kg=amount_kg,
                    price=price,
                    memo=memo,
                    orderLocationCode=location,
                    orderLocationName=location.codeName,
                    productCode=productCode,
                ).save()

        else:
            self.log(
                user=request.user,
                action="주문등록에러",
                obj=Order.objects.first(),
                extra=formset.errors[0]
            )
        return redirect('orderRegEx')

    def get(self, request):
        if not self.is_valid_order(request):
            messages.info(request, '주문 가능한 시간이 아닙니다.')
        orderForm = OrderFormExSet(request.GET or None)
        return render(request, 'order/orderRegEx.html', {'orderForm': orderForm})


class OrderListEx(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'order/orderListEx.html')


class ExcelUpload(LoginRequiredMixin, View):

    def post(self, request):
        excel_file = request.FILES.get('excelFile')
        wb: Workbook = load_workbook(excel_file, data_only=True)
        sheet1: Worksheet = wb['Sheet1']
        invalid_locations = []
        invalid_products = []

        for i, row in enumerate(sheet1.rows):
            if i > 1:
                ymd: str = row[0].value.strftime('%Y%m%d')
                locationName: str = row[1].value
                productName: str = row[2].value
                count: int = row[3].value
                memo: str = str(row[4].value)

                try:
                    location: Location = Location.objects.get(Q(codeName__contains=locationName.strip()), Q(type="05"))
                except Location.MultipleObjectsReturned as e:
                    location: Location = Location.objects.get(Q(codeName=locationName.strip()), Q(type="05"))
                except Location.DoesNotExist as e:
                    invalid_locations.append(i + 1)

                try:
                    productCode: ProductCode = ProductCode.objects.get(Q(codeName__contains=productName.strip()))
                except ProductCode.MultipleObjectsReturned as e:
                    productCode: ProductCode = ProductCode.objects.get(Q(codeName=productName.strip()))
                except ProductCode.DoesNotExist as e:
                    invalid_products.append(i + 1)

        if len(invalid_locations) > 0 or len(invalid_products) > 0:
            return JsonResponse([invalid_locations, invalid_products], safe=False, status=400)

        for i, row in enumerate(sheet1.rows):
            if i > 1:
                ymd: str = row[0].value.strftime('%Y%m%d')
                locationName: str = row[1].value
                productName: str = row[2].value
                count: int = row[3].value
                memo: str = str(row[4].value)

                try:
                    location: Location = Location.objects.get(Q(codeName__contains=locationName.strip()), Q(type="05"))
                except Location.MultipleObjectsReturned as e:
                    location: Location = Location.objects.get(Q(codeName=locationName.strip()), Q(type="05"))

                try:
                    productCode: ProductCode = ProductCode.objects.get(Q(codeName__contains=productName.strip()))
                except ProductCode.MultipleObjectsReturned as e:
                    productCode: ProductCode = ProductCode.objects.get(Q(codeName=productName.strip()))

                productUnitPrice = ProductUnitPrice.objects.get(Q(locationCode=location), Q(productCode=productCode))
                Order.objects.create(
                    ymd=ymd,
                    code=productCode.code,
                    codeName=productCode.codeName,
                    amount=productCode.amount_kg * count,
                    count=count,
                    amount_kg=productCode.amount_kg,
                    price=productUnitPrice.price,
                    memo=memo,
                    orderLocationCode=location,
                    orderLocationName=location.codeName,
                    productCode=productCode,
                ).save()

        return HttpResponse(status=200)
