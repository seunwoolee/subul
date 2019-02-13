from django import forms
from django.forms import formset_factory
from core.models import Location
from django_select2.forms import Select2Widget
from .models import ProductCode, ProductEgg, ProductMaster


class ProductUnitPricesForm(forms.Form):
    product = forms.ChoiceField(widget=Select2Widget,
                                choices=[('', '')] + list(ProductCode.objects.values_list('code', 'codeName')
                                                          .filter(delete_state='N').order_by('code')))
    location = forms.ChoiceField(widget=Select2Widget,
                                 choices=[('', '')] + list(Location.objects.values_list('code', 'codeName')
                                     .filter(delete_state='N').filter(type='05').order_by(
                                     'code')))
    price = forms.IntegerField(min_value=0)
    specialPrice = forms.IntegerField(min_value=0, required=False)

