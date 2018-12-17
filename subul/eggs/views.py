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
        releaseLocationForm = EggForm()
        return render(request, 'eggs/eggsList.html', {'releaseLocationForm': releaseLocationForm})


class EggReg(LoginRequiredMixin, View):

    def post(self, request):
        formset = EggFormSet(request.POST)

        if formset.is_valid():
            for form in formset:
                ymd = form.cleaned_data.get('ymd')
                code = form.cleaned_data.get('product')
                eggCode = EggCode.objects.get(code=code)
                codeName = eggCode.codeName
                count = form.cleaned_data.get('count')
                price = form.cleaned_data.get('price')
                memo = form.cleaned_data.get('memo')
                locationCode = Location.objects.get(code=form.cleaned_data.get('location'))
                locationCodeName = locationCode.codeName
                Egg.objects.create(
                    ymd=ymd,
                    code=code,
                    codeName=codeName,
                    count=count,
                    price=price,
                    memo=memo,
                    locationCode=locationCode,
                    locationCodeName=locationCodeName,
                    eggCode=eggCode,
                )
        else:
            print(formset.errors)
        form = OrderForm()
        return render(request, 'order/orderList.html', {'form': form})

    def get(self, request):
        eggForm = EggFormSet(request.GET or None)
        return render(request, 'eggs/eggsReg.html', {'eggForm': eggForm})
