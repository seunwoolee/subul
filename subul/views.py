from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin



class MainList(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'index.html')