from django.shortcuts import render
from django.views import View


class OrderList(View):
    def get(self, request):
        return render(request, 'order/orderList.html')