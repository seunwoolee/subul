from django.shortcuts import render
from django.views import View
from core.models import Location
from order.forms import OrderFormSet
from order.models import Order
from product.models import ProductCode, SetProductCode


class OrderList(View):
    def get(self, request):
        return render(request, 'order/orderList.html')

class OrderReg(View):

        def post(self, request):
            formset = OrderFormSet(request.POST)

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

                    if form.cleaned_data.get('package'):
                        setProduct = SetProductCode.objects.get(code=form.cleaned_data.get('package'))

                    if amount_kg * count == amount:
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
                        )

                        if setProduct:
                            order.setProduct = setProduct
                            order.save()

            else:
                print(formset.errors)
            return render(request, 'order/orderReg.html')

        def get(self, request):
            orderForm = OrderFormSet(request.GET or None)
            return render(request, 'order/orderReg.html', {'orderForm': orderForm})
