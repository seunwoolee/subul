from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic.base import View
from django.db.models import Q, F, ExpressionWrapper, Sum, DecimalField, When, Case, CharField, Value, IntegerField
from datetime import datetime
from datetime import timedelta

from eggs.models import EggOrder
from labor.forms import EggOrderForm

from product.forms import ProductOrderForm
from product.models import ProductOrder


class SiteEggOrder(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {}
        self.today = datetime.today().strftime('%Y%m%d')
        self.eggs = EggOrder.objects.filter(Q(display_state='Y'),Q(ymd=self.today)).order_by('id')
        self.form: EggOrderForm

    def get(self, request):

        if request.is_ajax() and request.GET.get('pk'):
            self.get_form(request.GET.get('pk'))
            return JsonResponse(self.data)

        if request.is_ajax():
            self.get_egg_list()
            return JsonResponse(self.data)
        else:
            return render(request, 'site/egg_index.html', {'eggs': self.eggs})

    def post(self, request, pk):
        eggOrder = get_object_or_404(EggOrder, pk=pk)
        egg_order: EggOrder = EggOrderForm(request.POST, instance=eggOrder).save()
        self.get_egg_list()
        return JsonResponse(self.data)

    def get_egg_list(self):
        self.data['list'] = render_to_string('site/partial_egg_order_list.html', {'eggs': self.eggs},
                                             request=self.request)

    def get_form(self, pk):
        eggOrder = get_object_or_404(EggOrder, pk=pk)
        self.form = EggOrderForm(instance=eggOrder)
        self.data['form'] = render_to_string('site/partial_egg_order_update.html', {'form': self.form},
                                             request=self.request)


class SiteProductOrder(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {}
        self.productOrders = self.get_query()
        self.max_count = 1

    def get(self, request):

        for productOrder in self.productOrders:
            current_count = productOrder.detail.filter(type='일반').count()
            if current_count > self.max_count:
                self.max_count = current_count

        self.get_product_list()

        if request.is_ajax():
            return JsonResponse(self.data)
        else:
            productOrderForm = ProductOrderForm()
            data = {'productOrders': self.productOrders, 'max_count': self.max_count,
                    'productOrderForm': productOrderForm}
            return render(request, 'site/product_index.html', data)

    def get_query(self):
        productOrders = ProductOrder.objects.filter(Q(display_state='Y'), Q(type__in=['전란', '난백난황'])) \
            .annotate(expire_memo=F('productCode__expiration')) \
            .annotate(real_count=Case(
            When(Q(past_stock__isnull=False) & Q(future_stock__isnull=False),
                 then=F('count') - F('past_stock__count') + F('future_stock__count')),
            When(Q(past_stock__isnull=True) & Q(future_stock__isnull=False),
                 then=F('count') + F('future_stock__count')),
            When(Q(past_stock__isnull=False) & Q(future_stock__isnull=True),
                 then=F('count') - F('past_stock__count')),
            default=F('count'), output_field=IntegerField())) \
            .annotate(real_amount=Case(
            When(Q(past_stock__isnull=False) & Q(future_stock__isnull=False),
                 then=F('amount') - F('past_stock__amount') + F('future_stock__amount')),
            When(Q(past_stock__isnull=True) & Q(future_stock__isnull=False),
                 then=F('amount') + F('future_stock__amount')),
            When(Q(past_stock__isnull=False) & Q(future_stock__isnull=True),
                 then=F('amount') - F('past_stock__amount')),
            default=F('amount'), output_field=DecimalField())).order_by('id')

        for productOrder in productOrders:
            total_boxCount = 0
            total_eaCount = 0

            for detail in productOrder.detail.filter(type='일반'):
                total_boxCount += detail.boxCount
                total_eaCount += detail.eaCount

                if detail.future_stock:
                    total_boxCount += detail.future_stock.boxCount
                    total_eaCount += detail.future_stock.eaCount

                if detail.past_stock:
                    total_boxCount -= detail.past_stock.boxCount
                    total_eaCount -= detail.past_stock.eaCount

            yyyy, mm, dd = int(productOrder.ymd[0:4]), int(productOrder.ymd[4:6]), int(productOrder.ymd[6:])
            ymd = datetime(yyyy, mm, dd)
            expire_date = ymd + timedelta(days=productOrder.expire_memo)
            productOrder.expire_memo = f'유통기한({productOrder.expire_memo})일 / {expire_date.strftime("%Y-%m-%d")}'
            productOrder.total_boxCount = total_boxCount
            productOrder.total_eaCount = total_eaCount
        return productOrders

    def get_product_list(self):
        data = {'productOrders': self.productOrders, 'max_count': self.max_count}
        self.data['list'] = render_to_string('site/partial_product_order_list.html', data, request=self.request)


class Nav(View):

    def get(self, request):
        return render(request, 'site/nav_index.html')
