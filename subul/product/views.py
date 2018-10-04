from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.base import View
from .forms import StepOneForm , StepTwoForm , StepThreeForm , StepFourForm , StepFourFormSet ,  Select2WidgetForm
from django.views.generic import FormView
# class HomePageView(TemplateView):
#     template_name = 'product/home.html'

class TemplateFormView(View):

    def get(self, request):
        form = Select2WidgetForm(auto_id=False)
        template_name = 'product/form.html'
        return render(request, template_name, {'form':form})

class ProductView(View):

    def post(self, request):
        print(request.POST)
        return render(request, 'product/home.html')

    def get(self, request):
        stepOneForm = StepOneForm(auto_id=False)
        stepTwoForm = StepTwoForm(auto_id=False)
        stepThreeForm = StepThreeForm(auto_id=False)
        stepFourForm = StepFourFormSet(request.GET or None)

        testValue = '12222'
        return render(request, 'product/home.html',{'stepOneForm' : stepOneForm,
                                                       'stepTwoForm' : stepTwoForm,
                                                       'stepThreeForm' : stepThreeForm,
                                                       'stepFourForm' : stepFourForm,
                                                       'testValue' : testValue})