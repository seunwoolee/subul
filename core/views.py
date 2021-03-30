from django import core
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View

from eventlog.models import LogginMixin
from users.models import CustomUser
from .models import Location, OrderTime
from .forms import LocationForm, OrderTimeFormSet
from django.contrib.auth.mixins import LoginRequiredMixin


class LocationList(LoginRequiredMixin, View):

    def get(self, request):
        form = LocationForm()
        return render(request, 'code/locationList.html', {'form': form})


class LocationReg(LogginMixin, LoginRequiredMixin, View):

    def post(self, request):
        formset = LocationForm(request.POST)
        if formset.is_valid():
            code = str(int(Location.objects.order_by('-code').first().code) + 1)
            code = '00' + code if len(code) == 3 else '0' + code
            form = formset.save(commit=False)
            form.code = code
            form.save()
        else:
            self.log(
                user=request.user,
                action="장소등록에러",
                obj=Location.objects.first(),
                extra=formset.errors[0]
            )
        return redirect('locationReg')

    def get(self, request):
        form = LocationForm(request.GET or None)
        return render(request, 'code/locationReg.html', {'form': form})


class Audit(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'code/audit.html')


class OrderTimeReg(LoginRequiredMixin, View):
    def post(self, request):
        formset = OrderTimeFormSet(request.POST)

        if formset.is_valid():
            for form in formset:
                user_id = form.cleaned_data.get('company')
                weekday = form.cleaned_data.get('weekday')
                start: str = form.cleaned_data.get('start')
                end: str = form.cleaned_data.get('end')

                # start_list: list = start.split(':')
                # end_list: list = end.split(':')

                # start = start_list[0] + start_list[1]
                # end = end_list[0] + end_list[1]
                company = CustomUser.objects.get(id=user_id)

                OrderTime.objects.filter(Q(company=company), Q(weekday=weekday)).delete()

                OrderTime.objects.create(
                    company=company,
                    company_name=company.username,
                    weekday=weekday,
                    start=start,
                    end=end
                ).save()

        return redirect('orderTimeReg')

    def get(self, request):
        orderTimeForm = OrderTimeFormSet(request.GET or None)
        return render(request, 'code/orderTime.html', {'orderTimeForm': orderTimeForm})


class OrderTimeList(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'code/orderTimeList.html')
