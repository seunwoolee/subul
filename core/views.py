from django.shortcuts import render, redirect
from django.views import View

from eventlog.models import LogginMixin
from .models import Location
from .forms import LocationForm
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
