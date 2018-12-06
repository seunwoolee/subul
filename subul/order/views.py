from django.shortcuts import render
from django.views import View
from core.models import Location
from order.forms import OrderFormSet, OrderForm
from order.models import Order
from product.models import ProductCode, SetProductCode
from django.db.models import Sum, F, ExpressionWrapper, FloatField, IntegerField, Func
from core.utils import render_to_pdf
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class Round(Func):
    function = 'ROUND'
    # template = '%(function)s(%(expressions)s, 0)'


class GeneratePDF(View):

    def get(self, request, *args, **kwargs):
        ymd = request.GET['ymd']
        yyyymmdd = "{}/{}/{}".format(ymd[0:4], ymd[4:6], ymd[6:])
        orderLocationCode = request.GET['orderLocationCode']
        # template = get_template('invoice/거래명세표.html')
        location = Location.objects.get(code=orderLocationCode)
        orders = Order.objects.filter(ymd=ymd).filter(orderLocationCode=location) \
            .values('code', 'codeName', 'price', 'specialTag') \
            .annotate(totalCount=Sum('count')) \
            .annotate(totalPrice=F('totalCount') * F('price')) \
            .annotate(vat=ExpressionWrapper(F('productCode__vat') * 0.01 + 1, output_field=FloatField())) \
            .annotate(supplyPrice=ExpressionWrapper(Round(F('totalPrice') / F('vat')), output_field=IntegerField())) \
            .annotate(vatPrice=F('totalPrice') - F('supplyPrice'))
        sumTotalCount = orders.aggregate(sumTotalCount=Sum('totalCount'))
        sumSupplyPrice = orders.aggregate(sumSupplyPrice=Sum('supplyPrice'))
        sumVat = orders.aggregate(sumVat=Sum('vatPrice'))
        sumTotal = sumSupplyPrice['sumSupplyPrice'] + sumVat['sumVat']
        sumData = {'sumTotalCount': sumTotalCount['sumTotalCount'],
                   'sumSupplyPrice': sumSupplyPrice['sumSupplyPrice'],
                   'sumVat': sumVat['sumVat'],
                   'sumTotal': sumTotal}
        context_dict = {
            "yyyymmdd": yyyymmdd,
            "orders": orders,
            "sumData": sumData,
            "location": location,
        }
        # html = template.render(context_dict)
        pdf = render_to_pdf('invoice/주문거래명세표.html', context_dict)
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


class OrderList(LoginRequiredMixin, View):

    def get(self, request):
        print(request.user.has_perm('order.delete_order')) # TODO 권한 문제!!
        form = OrderForm()
        return render(request, 'order/orderList.html', {'form': form})


class OrderReg(LoginRequiredMixin, View):

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
                specialTag = form.cleaned_data.get('specialTag')

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
                        specialTag=specialTag,
                        productCode=productCode,
                    )

                    if setProduct:
                        order.setProduct = setProduct
                        order.save()

        else:
            print(formset.errors)
        form = OrderForm()
        return render(request, 'order/orderList.html', {'form': form})

    def get(self, request):
        orderForm = OrderFormSet(request.GET or None)
        return render(request, 'order/orderReg.html', {'orderForm': orderForm})
