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
        self.eggs = EggOrder.objects.filter(display_state='Y')
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
        self.data['list'] = render_to_string('site/partial_egg_order_list.html', {'eggs': self.eggs}, request=self.request)

    def get_form(self, pk):
        eggOrder = get_object_or_404(EggOrder, pk=pk)
        self.form = EggOrderForm(instance=eggOrder)
        self.data['form'] = render_to_string('site/partial_egg_order_update.html', {'form': self.form}, request=self.request)


class SiteProductOrder(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {}
        self.productOrders = self.get_query()
        self.max_count = 1

    def get(self, request):

        for productOrder in self.productOrders:
            if productOrder.detail.all().count() > self.max_count:
                self.max_count = productOrder.detail.all().count()

        self.get_product_list()

        if request.is_ajax():
            return JsonResponse(self.data)
        else:
            productOrderForm = ProductOrderForm()
            data = {'productOrders': self.productOrders, 'max_count': self.max_count, 'productOrderForm': productOrderForm}
            return render(request, 'site/product_index.html', data)

    def get_query(self):
        productOrders = ProductOrder.objects.filter(display_state='Y').annotate(expire_memo=F('productCode__expiration'))
        for productOrder in productOrders:
            yyyy,mm, dd = int(productOrder.ymd[0:4]), int(productOrder.ymd[4:6]), int(productOrder.ymd[6:])
            ymd = datetime(yyyy, mm, dd)
            expire_date = ymd + timedelta(days=productOrder.expire_memo)
            productOrder.expire_memo = f'유통기한({productOrder.expire_memo})일 / {expire_date.strftime("%Y-%m-%d")}'
        return productOrders

    def get_product_list(self):
        data = {'productOrders': self.productOrders, 'max_count': self.max_count}
        self.data['list'] = render_to_string('site/partial_product_order_list.html', data, request=self.request)


class Nav(View):

    def get(self, request):
        return render(request, 'site/nav_index.html')
