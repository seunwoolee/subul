from django.db.models import Sum, Func, Value, CharField
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from core.models import Location
from eventlog.models import LogginMixin
from labor.forms import EggOrderModifyForm
from order.models import ABS
from .forms import EggForm
from .models import Egg, EggCode, EggOrder
from .forms import EggFormSet
from django.contrib.auth.mixins import LoginRequiredMixin
from core.utils import render_to_pdf


class Round(Func):
    function = 'ROUND'


class EggList(LoginRequiredMixin, View):
    def get(self, request):
        eggForm = EggForm()
        eggModifyForm = EggOrderModifyForm()
        return render(request, 'eggs/eggsList.html', {'eggForm': eggForm, 'eggModifyForm': eggModifyForm})


class EggReg(LogginMixin, LoginRequiredMixin, View):

    def post(self, request):
        formset = EggFormSet(request.POST)
        self.log(
            user=request.user,
            action="원란등록",
            obj=Egg.objects.first(),
            extra=request.POST
        )
        if formset.is_valid():
            for form in formset:
                in_ymd = form.cleaned_data.get('in_ymd')
                code = form.cleaned_data.get('product')
                eggCode = EggCode.objects.get(code=code)
                codeName = eggCode.codeName
                count = form.cleaned_data.get('count')
                price = form.cleaned_data.get('price')
                memo = form.cleaned_data.get('memo')
                locationCode = Location.objects.get(code=form.cleaned_data.get('location'))
                locationCodeName = locationCode.codeName
                Egg.objects.create(
                    in_ymd=in_ymd,
                    ymd=in_ymd,
                    code=code,
                    codeName=codeName,
                    count=count,
                    price=price,
                    memo=memo,
                    in_locationCode=locationCode,
                    in_locationCodeName=locationCodeName,
                    eggCode=eggCode,
                )
        else:
            print(formset.errors)
        return redirect('eggsList')

    def get(self, request):
        eggForm = EggFormSet(request.GET or None)
        return render(request, 'eggs/eggsReg.html', {'eggForm': eggForm})


class EggRelease(LogginMixin, View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pks: list = []

    def post(self, request):
        self.amount = request.POST.get('amount', None)
        self.order = request.POST.get('order', None)
        self.data: dict = dict(request.POST.copy())
        print(self.data)
        self.user = request.user

        if self.order:
            self.log(
                user=request.user,
                action="원란지시",
                obj=Egg.objects.first(),
                extra=self.data
            )
            self.order_egg()
        else:
            self.log(
                user=request.user,
                action="원란출고",
                obj=Egg.objects.first(),
                extra=self.data
            )
            self.save_egg()
            if self.pks:
                pks = ','.join(self.pks)
                Egg.calculateAmount(int(self.amount), pks)

        return HttpResponse(status=200)

    def save_egg(self):
        for i in range(len(self.data['in_ymd'])):
            in_ymd: str = self.data['in_ymd'][i]
            ymd: str = self.data['ymd'][i]
            productCode: str = self.data['productCode'][i]
            in_location: str = self.data['in_location'][i]
            type: str = self.data['type'][i]
            count: int = int(self.data['count'][i])
            location: str = self.data['locationSale'][i]
            price: int = self.data['price'][i]
            memo: str = self.data['memo'][i]

            product = EggCode.objects.get(code=productCode)
            in_location: Location = Location.objects.get(code=in_location)
            egg: Egg = Egg.objects.create(
                in_ymd=in_ymd,
                code=productCode,
                codeName=product.codeName,
                in_locationCode=in_location,
                in_locationCodeName=in_location.codeName,
                type=type,
                ymd=ymd,
                count=-count,
                eggCode=product,
                memo=memo,
            )

            if location:
                location: Location = Location.objects.get(code=location)
                egg.locationCode = location
                egg.locationCodeName = location.codeName

            if price:
                egg.price = price

            egg.save()
            if self.amount:
                if egg.type == '생산':
                    self.pks.append(str(egg.id))

    def order_egg(self):
        for i in range(len(self.data['in_ymd'])):
            in_ymd: str = self.data['in_ymd'][i]
            ymd: str = self.data['ymd'][i]
            productCode: str = self.data['productCode'][i]
            in_location: str = self.data['in_location'][i]
            count: int = int(self.data['count'][i])
            memo: str = self.data['memo'][i]

            product = EggCode.objects.get(code=productCode)
            in_location: Location = Location.objects.get(code=in_location)
            EggOrder(ymd=ymd,
                     code=productCode,
                     codeName=product.codeName,
                     orderCount=count,
                     memo=memo,
                     eggCode=product,
                     in_ymd=in_ymd,
                     in_locationCode=in_location,
                     in_locationCodeName=in_location.codeName).save()


class EggCalculateAmount(LogginMixin, View):
    def post(self, request):
        data = request.POST.dict()
        self.log(
            user=request.user,
            action="원란중량계산",
            obj=Egg.objects.first(),
            extra=data
        )
        amount = int(data['amount'])
        pks = data['pks']
        Egg.calculateAmount(amount, pks)
        return HttpResponse(status=200)


class EggPricePerEa(LogginMixin, View):
    def post(self, request):
        data = request.POST.dict()
        self.log(
            user=request.user,
            action="원란생산단가작업",
            obj=Egg.objects.first(),
            extra=data
        )
        eggs = Egg.objects.filter(ymd__gte=data['start_date']).filter(ymd__lte=data['end_date']).filter(type='생산')
        for egg in eggs:
            in_price = Egg.objects.values('price', 'count').filter(in_ymd=egg.in_ymd).filter(type='입고') \
                .filter(code=egg.code).filter(in_locationCode=egg.in_locationCode).first()
            egg.price = round(in_price['price'] / in_price['count']) * abs(
                egg.count)  # 구매단가=in_price['price']/abs(egg.count)
            egg.save()
        return HttpResponse(status=200)


class GeneratePDF(View):

    def get(self, request, *args, **kwargs):
        ymd = request.GET['ymd']
        yyyymmdd = "{}/{}/{}".format(ymd[0:4], ymd[4:6], ymd[6:])
        locationCode = request.GET['locationCode']
        moneyMark = request.GET['moneyMark']
        location = Location.objects.get(code=locationCode)
        eggs = Egg.objects.filter(ymd=ymd).filter(locationCode=location) \
            .values('code', 'codeName', 'price', 'memo') \
            .annotate(totalCount=ABS('count'))
        sumTotalCount = eggs.aggregate(sumTotalCount=Sum('totalCount'))
        sumSupplyPrice = 0
        sumVat = 0
        sumTotal = eggs.aggregate(sumTotalPrice=Sum('price'))
        sumData = {'sumTotalCount': sumTotalCount['sumTotalCount'],
                   'sumSupplyPrice': sumSupplyPrice,
                   'sumVat': sumVat,
                   'sumTotal': sumTotal['sumTotalPrice'],
                   'moneyMark': moneyMark}
        context_dict = {
            "yyyymmdd": yyyymmdd,
            "eggs": eggs,
            "sumData": sumData,
            "location": location,
        }
        pdf = render_to_pdf('invoice/원란거래명세표.html', context_dict)
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


class EggReport(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.arr = []
        self.codeName = ''
        self.previous_stock_sum = 0
        self.in_sum = 0
        self.insert_sum = 0
        self.release_sum = 0
        self.current_stock_sum = 0

        self.total_previous_stock_sum = 0
        self.total_in_sum = 0
        self.total_insert_sum = 0
        self.total_release_sum = 0
        self.total_current_stock_sum = 0

    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        egg_previous = Egg.objects.values('code', 'codeName', 'in_ymd', 'in_locationCodeName') \
            .annotate(totalCount=Sum('count')).annotate(gubun=Value('previous', output_field=CharField())) \
            .filter(ymd__lt=start_date) \
            .filter(totalCount__gt=0).order_by('eggCode__sorts', 'in_ymd')
        egg_period = Egg.objects.values('code', 'codeName', 'in_ymd', 'in_locationCodeName') \
            .annotate(totalCount=Sum('count')).annotate(gubun=Value('period', output_field=CharField())) \
            .filter(ymd__gte=start_date) \
            .filter(ymd__lte=end_date) \
            .filter(type='입고') \
            .order_by('eggCode__sorts', 'in_ymd')
        queryset = egg_previous.union(egg_period)
        queryset = queryset.order_by('code')
        self.codeName = queryset[0]['codeName']
        last_index = len(queryset)
        for i, egg in enumerate(queryset):
            result = {}
            countPerType = Egg.objects.values('code', 'codeName', 'in_ymd', 'in_locationCodeName', 'type') \
                .annotate(totalCount=Sum('count')) \
                .annotate(totalPrice=Sum('price')) \
                .filter(code=egg['code']) \
                .filter(in_ymd=egg['in_ymd']) \
                .filter(in_locationCodeName=egg['in_locationCodeName']) \
                .filter(ymd__gte=start_date) \
                .filter(ymd__lte=end_date)

            PREVIOUS_STOCK = egg["totalCount"] if egg['gubun'] == 'previous' else 0
            IN = 0
            INSERT = 0
            OTHER = 0
            for element in countPerType:
                number = element["totalCount"]
                if element['type'] == '생산':
                    INSERT += number
                elif element['type'] == '입고':
                    IN += number
                else:
                    OTHER += number

            RELEASE = INSERT + OTHER
            CURRENT_STOCK = IN + PREVIOUS_STOCK + RELEASE
            if INSERT:
                INSERT = abs(int(INSERT))
            else:
                INSERT = ''
            if IN:
                IN = abs(int(IN))
            else:
                IN = ''
            if RELEASE:
                RELEASE = abs(int(RELEASE))
            else:
                RELEASE = ''

            if self.codeName == egg['codeName']:
                result['codeName'] = egg['codeName']
                result['in_ymd'] = '{}/{}'.format(egg['in_ymd'][4:6], egg['in_ymd'][6:8])
                result['in_locationCodeName'] = egg['in_locationCodeName']
                if PREVIOUS_STOCK:
                    result['previousStock'] = PREVIOUS_STOCK
                else:
                    result['previousStock'] = ''
                result['in'] = IN
                result['insert'] = INSERT
                result['release'] = RELEASE
                if CURRENT_STOCK:
                    result['currentStock'] = CURRENT_STOCK
                else:
                    result['currentStock'] = ''
                self.arr.append(result)
                self.increase_sum_data(PREVIOUS_STOCK, IN, INSERT, RELEASE, CURRENT_STOCK)
            else:
                self.insert_sum_data(egg['codeName'])
                self.reset_sum_data(egg['codeName'], PREVIOUS_STOCK, IN, INSERT, RELEASE, CURRENT_STOCK)
                result = {}
                result['codeName'] = egg['codeName']
                result['in_ymd'] = '{}/{}'.format(egg['in_ymd'][4:6], egg['in_ymd'][6:8])
                result['in_locationCodeName'] = egg['in_locationCodeName']
                if PREVIOUS_STOCK:
                    result['previousStock'] = PREVIOUS_STOCK
                else:
                    result['previousStock'] = ''
                result['in'] = IN
                result['insert'] = INSERT
                result['release'] = RELEASE
                if CURRENT_STOCK:
                    result['currentStock'] = CURRENT_STOCK
                else:
                    result['currentStock'] = ''
                self.arr.append(result)

            if i == last_index - 1:
                self.insert_sum_data(egg['codeName'])

        self.insert_total_sum_data()
        if len(self.arr) > 37:
            first_loop_reuslt = self.arr[:37]
            loop_reuslt = self.arr[37:]
            return render(request, 'eggs/eggsReport.html',
                          {'first_loop_reuslt': first_loop_reuslt,
                           'loop_reuslt': loop_reuslt,
                           'start_date': start_date,
                           'end_date': end_date})
        else:  # 한장짜리
            return render(request, 'eggs/eggsReport.html', {'result_list': self.arr,
                                                            'start_date': start_date,
                                                            'end_date': end_date})

    def insert_sum_data(self, codeName):
        result = {}
        result['codeName'] = '소계'
        if self.previous_stock_sum:
            result['previousStock'] = self.previous_stock_sum
        else:
            result['previousStock'] = 0
        result['in'] = self.in_sum
        result['insert'] = self.insert_sum
        result['release'] = self.release_sum
        if self.current_stock_sum:
            result['currentStock'] = self.current_stock_sum
        else:
            result['currentStock'] = 0

        self.total_previous_stock_sum += self.previous_stock_sum
        self.total_in_sum += self.in_sum
        self.total_insert_sum += self.insert_sum
        self.total_release_sum += self.release_sum
        self.total_current_stock_sum += self.current_stock_sum
        self.arr.append(result)

    def increase_sum_data(self, *args):
        self.previous_stock_sum += args[0]
        if args[1]: self.in_sum += args[1]
        if args[2]: self.insert_sum += args[2]
        if args[3]: self.release_sum += args[3]
        if args[4]: self.current_stock_sum += args[4]

    def reset_sum_data(self, *args):
        self.codeName = args[0]
        self.previous_stock_sum = int(args[1]) if args[1] else 0
        self.in_sum = int(args[2]) if args[2] else 0
        self.insert_sum = int(args[3]) if args[3] else 0
        self.release_sum = int(args[4]) if args[4] else 0
        self.current_stock_sum = int(args[5]) if args[5] else 0

    def insert_total_sum_data(self):
        result = {}
        result['codeName'] = '합계'
        if self.total_previous_stock_sum:
            result['previousStock'] = self.total_previous_stock_sum
        else:
            result['previousStock'] = ''
        result['in'] = self.total_in_sum
        result['insert'] = self.total_insert_sum
        result['release'] = self.total_release_sum
        if self.total_current_stock_sum:
            result['currentStock'] = self.total_current_stock_sum
        else:
            result['currentStock'] = ''
        self.arr.append(result)
