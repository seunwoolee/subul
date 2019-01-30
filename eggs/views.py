
from django.db.models import Sum, Func, F
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from core.models import Location
from order.forms import OrderForm
from .forms import EggForm
from .models import Egg, EggCode
from .forms import EggFormSet
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from core.utils import render_to_pdf


class Round(Func):
    function = 'ROUND'
    # template = '%(function)s(%(expressions)s, 0)'


class ABS(Func):
    function = 'ABS'
    # template = '%(function)s(%(expressions)s, 0)'


class EggList(View):

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
                print(memo)
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
        data = request.POST.dict()
        try:
            location = data['locationSale']
            price = data['price']
        except KeyError:
            location = None
            price = None

        product = EggCode.objects.get(code=data['productCode'])
        in_location = Location.objects.get(code=data['in_locatoin'])
        egg = Egg.objects.create(
            in_ymd=data['in_ymd'],
            code=data['productCode'],
            codeName=product.codeName,
            in_locationCode=in_location,
            in_locationCodeName=in_location.codeName,
            type=data['type'],
            ymd=data['ymd'],
            count=-int(data['count']),
            eggCode=product
        )

        if location:
            location = Location.objects.get(code=location)
            egg.locationCode = location
            egg.locationCodeName = location.codeName

        if price:
            egg.price = price

        egg.save()
        return HttpResponse(status=200)


class EggCalculateAmount(View):
    def post(self, request):
        data = request.POST.dict()
        amount = data['amount']
        pks = data['pks']
        arr = pks.split(',')
        eggs = Egg.objects.filter(id__in=arr)
        totalCount = Egg.objects.filter(id__in=arr).aggregate(Sum('count'))

        for egg in eggs:
            percent = round((egg.count / totalCount['count__sum']), 2)
            egg_amount = round(percent * int(amount), 2)
            egg.amount = egg_amount
            egg.save()
        return HttpResponse(status=200)


class EggPricePerEa(View):
    def post(self, request):
        data = request.POST.dict()
        eggs = Egg.objects.filter(ymd__gte=data['start_date']).filter(ymd__lte=data['end_date']).filter(type='생산')

        for egg in eggs:
            in_price = Egg.objects.values('price','count').filter(in_ymd=egg.in_ymd).filter(type='입고').filter(code=egg.code)\
                .filter(in_locationCode=egg.in_locationCode).first()
            egg.price = round(in_price['price'] / in_price['count']) * abs(egg.count) # 구매단가=in_price['price']/abs(egg.count)
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
            filename = "Invoice%s.pdf" % ("")
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
