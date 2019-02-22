from django import forms
from django.forms import formset_factory
from core.models import Location
from django_select2.forms import Select2Widget
from .models import ProductCode, ProductEgg, ProductMaster


class ProductUnitPricesForm(forms.Form):
    location = forms.ChoiceField(widget=Select2Widget,
                                 choices=[('', '')] + list(Location.objects.values_list('code', 'codeName')
                                     .filter(delete_state='N').filter(type='05').order_by('code')))
    locationCode = forms.CharField(widget=forms.HiddenInput())
    product = forms.ChoiceField(widget=Select2Widget,
                                choices=[('', '')] + list(ProductCode.objects.values_list('code', 'codeName')
                                                          .filter(delete_state='N').order_by('code')))
    productCode = forms.CharField(widget=forms.HiddenInput())
    price = forms.IntegerField(min_value=0)
    specialPrice = forms.IntegerField(min_value=0, required=False)

