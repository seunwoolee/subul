from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from core.models import Location
from order.forms import OrderForm
from .forms import EggForm
from .models import Egg, EggCode
from .forms import EggFormSet
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


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
        form = OrderForm()
        return render(request, 'order/orderList.html', {'form': form})

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