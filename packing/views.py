from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from core.models import Location
from eggs.forms import EggForm
from eventlog.models import LogginMixin
from .models import Packing, PackingCode
from .forms import PackingFormSet, PackingForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class PackingList(LogginMixin, LoginRequiredMixin, View):

    def get(self, request):
        packingForm = PackingForm()
        return render(request, 'packing/packingList.html', {'packingForm': packingForm})


class PackingReg(LogginMixin, LoginRequiredMixin, View):

    def post(self, request):
        formset = PackingFormSet(request.POST)
        log_data = request.POST
        self.log(
            user=request.user,
            action="포장재등록",
            obj=Packing.objects.first(),
            extra=log_data
        )
        if formset.is_valid():
            for form in formset:
                ymd = form.cleaned_data.get('ymd')
                code = form.cleaned_data.get('product')
                packingCode = PackingCode.objects.get(code=code)
                codeName = packingCode.codeName
                count = form.cleaned_data.get('count')
                price = form.cleaned_data.get('price')
                memo = form.cleaned_data.get('memo')
                locationCode = Location.objects.get(code=form.cleaned_data.get('location'))
                locationCodeName = locationCode.codeName
                Packing.objects.create(
                    ymd=ymd,
                    code=code,
                    codeName=codeName,
                    count=count,
                    price=price,
                    memo=memo,
                    locationCode=locationCode,
                    locationCodeName=locationCodeName,
                    packingCode=packingCode,
                )
        else:
            self.log(
                user=request.user,
                action="포장재등록에러",
                obj=Packing.objects.first(),
                extra=formset.errors[0]
            )
        return redirect('packingList')

    def get(self, request):
        packingForm = PackingFormSet(request.GET or None)
        return render(request, 'packing/packingReg.html', {'packingForm': packingForm})


class PackingRelease(View):
    def post(self, request):
        data = request.POST.dict()
        product = PackingCode.objects.get(code=data['code'])
        Packing.objects.create(
            ymd=data['ymd'],
            type=data['type'],
            code=product.code,
            codeName=product.codeName,
            count=-int(data['count']),
            packingCode=product,
            memo=data['memo']
        )
        return HttpResponse(status=200)
