from django.db.models import Sum, Func, F
from django.http import HttpResponse, QueryDict
from django.shortcuts import render, redirect
from django.views import View

from core.models import Location
from .forms import EggForm
from .models import Egg, EggCode
from .forms import EggFormSet
from django.contrib.auth.mixins import LoginRequiredMixin
from core.utils import render_to_pdf


class Round(Func):
    function = 'ROUND'


class ABS(Func):
    function = 'ABS'


class EggList(LoginRequiredMixin, View):

    def get(self, request):
        eggForm = EggForm()
        return render(request, 'eggs/eggsList.html', {'eggForm': eggForm})


class EggReg(LoginRequiredMixin, View):

    def post(self, request):
        formset = EggFormSet(request.POST)

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


class EggRelease(View):
    def post(self, request):
        amount = request.POST.get('amount', None)
        data = dict(request.POST.copy())
        pks = []

        for i in range(len(data['in_ymd'])):
            in_ymd = data['in_ymd'][i]
            ymd = data['ymd'][i]
            productCode = data['productCode'][i]
            in_location = data['in_location'][i]
            type = data['type'][i]
            count = data['count'][i]
            location = data['locationSale'][i]
            price = data['price'][i]
            memo = data['memo'][i]

            product = EggCode.objects.get(code=productCode)
            in_location = Location.objects.get(code=in_location)
            egg = Egg.objects.create(
                in_ymd=in_ymd,
                code=productCode,
                codeName=product.codeName,
                in_locationCode=in_location,
                in_locationCodeName=in_location.codeName,
                type=type,
                ymd=ymd,
                count=-int(count),
                eggCode=product,
                memo=memo,
            )

            if location:
                location = Location.objects.get(code=location)
                egg.locationCode = location
                egg.locationCodeName = location.codeName

            if price:
                egg.price = price

            egg.save()
            if amount:
                if egg.type == '생산':
                    pks.append(str(egg.id))

        if pks:
            pks = ','.join(pks)
            Egg.calculateAmount(int(amount), pks)

        return HttpResponse(status=200)


class EggCalculateAmount(View):
    def post(self, request):
        data = request.POST.dict()
        amount = int(data['amount'])
        pks = data['pks']
        Egg.calculateAmount(amount, pks)
        return HttpResponse(status=200)


class EggPricePerEa(View):
    def post(self, request):
        data = request.POST.dict()
        eggs = Egg.objects.filter(ymd__gte=data['start_date']).filter(ymd__lte=data['end_date']).filter(type='생산')

        for egg in eggs:
            in_price = Egg.objects.values('price', 'count').filter(in_ymd=egg.in_ymd).filter(type='입고').filter(
                code=egg.code) \
                .filter(in_locationCode=egg.in_locationCode).first()
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
        # html = template.render(context_dict)
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
    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        arr = []
        egg_previous = Egg.objects.values('code', 'codeName', 'in_ymd', 'in_locationCodeName') \
            .annotate(totalCount=Sum('count')) \
            .filter(ymd__lt=start_date) \
            .filter(totalCount__gt=0).order_by('eggCode__sorts', 'in_ymd')  # 재고가 0초과인 이전 재고
        egg_period = Egg.objects.values('code', 'codeName', 'in_ymd', 'in_locationCodeName') \
            .annotate(totalCount=Sum('count')) \
            .filter(ymd__gte=start_date) \
            .filter(ymd__lte=end_date) \
            .filter(type='입고') \
            .order_by('eggCode__sorts', 'in_ymd')
        queryset = egg_previous.union(egg_period)
        queryset = queryset.order_by('code')
        print(queryset)

        for egg in queryset:
            result = {}
            countPerType = Egg.objects.values('code', 'codeName', 'in_ymd', 'in_locationCodeName', 'type') \
                .annotate(totalCount=Sum('count')) \
                .annotate(totalPrice=Sum('price')) \
                .filter(code=egg['code']) \
                .filter(in_ymd=egg['in_ymd']) \
                .filter(in_locationCodeName=egg['in_locationCodeName']) \
                .filter(ymd__gte=start_date) \
                .filter(ymd__lte=end_date)

            PREVIOUS_STOCK = egg["totalCount"]
            INSERT = 0
            OTHER = 0
            for element in countPerType:  # 전일재고니깐 생성 없음
                number = element["totalCount"]
                if element['type'] == '생산':
                    INSERT += number
                else:
                    OTHER += number

            RELEASE = INSERT + OTHER
            CURRENT_STOCK = PREVIOUS_STOCK + RELEASE
            if INSERT == 0: INSERT = None
            if OTHER == 0: OTHER = None
            if RELEASE == 0: RELEASE = None
            result['codeName'] = egg['codeName']
            result['in_ymd'] = egg['in_ymd']
            result['in_locationCodeName'] = egg['in_locationCodeName']
            result['previousStock'] = PREVIOUS_STOCK
            result['in'] = None
            result['insert'] = INSERT
            result['release'] = RELEASE
            result['currentStock'] = CURRENT_STOCK
            arr.append(result)

        if len(arr) > 37:
            first_loop_reuslt = arr[:37]
            loop_reuslt = arr[37:]
            return render(request, 'eggs/eggsReport.html',
                          {'first_loop_reuslt': first_loop_reuslt,
                           'loop_reuslt': loop_reuslt,
                           'start_date': start_date,
                           'end_date': end_date})
        else: # 한장짜리
            return render(request, 'eggs/eggsReport.html', {'result_list': arr,
                                                                'start_date': start_date,
                                                                'end_date': end_date})