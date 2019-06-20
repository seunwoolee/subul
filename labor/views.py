from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic.base import View

from eggs.models import EggOrder
from labor.forms import EggOrderForm


# @method_decorator(csrf_exempt, name='dispatch')
class SiteList(LoginRequiredMixin, View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {}
        self.eggs = EggOrder.objects.filter(display_state='Y')
        self.form: EggOrderForm
        # self.request_type = 'get'

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