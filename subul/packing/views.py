from django.shortcuts import render
from django.views import View

from core.models import Location
from order.forms import OrderForm
from .models import Packing, PackingCode
from .forms import PackingFormSet
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


# class OrderList(LoginRequiredMixin, View):
#
#     def get(self, request):
#         print(request.user.has_perm('order.delete_order')) # TODO 권한 문제!!
#         form = OrderForm()
#         return render(request, 'order/orderList.html', {'form': form})


class PackingReg(LoginRequiredMixin, View):

    def post(self, request):
        formset = PackingFormSet(request.POST)

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
            print(formset.errors)
        form = OrderForm()
        return render(request, 'order/orderList.html', {'form': form})

    def get(self, request):
        packingForm = PackingFormSet(request.GET or None)
        return render(request, 'packing/packingReg.html', {'packingForm': packingForm})
