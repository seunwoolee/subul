from django import forms
from django.forms import formset_factory
from core.models import Location
from django_select2.forms import Select2Widget
from .models import ProductCode, ProductEgg, ProductMaster, SetProductCode


class ProductUnitPricesForm(forms.Form):
    location = forms.ChoiceField(widget=Select2Widget,
                                 choices=[('', '')] + list(Location.objects.values_list('code', 'codeName')
                                     .filter(delete_state='N').filter(type='05').order_by('code')))
    product = forms.ChoiceField(widget=Select2Widget,
                                choices=[('', '')] + list(ProductCode.objects.values_list('code', 'codeName')
                                                          .filter(delete_state='N').order_by('code')))
    price = forms.IntegerField(min_value=0)
    specialPrice = forms.IntegerField(min_value=0, required=False)
    locationCode = forms.CharField(widget=forms.HiddenInput()) # 생성 form
    productCode = forms.CharField(widget=forms.HiddenInput()) # 생성 form


class SetProductMatchForm(forms.Form):
    location = forms.ChoiceField(widget=Select2Widget,
                                 choices=[('', '')] + list(Location.objects.values_list('code', 'codeName')
                                     .filter(delete_state='N').filter(type='05').order_by('code')))
    setProduct = forms.ChoiceField(widget=Select2Widget,
                                   choices=[('', '')] + list(SetProductCode.objects.values_list('code', 'codeName')
                                                          .filter(delete_state='N').order_by('code')))
    product = forms.ChoiceField(widget=Select2Widget,
                                choices=[('', '')] + list(ProductCode.objects.values_list('code', 'codeName')
                                                          .filter(delete_state='N').order_by('code')))
    price = forms.IntegerField(min_value=0)
    count = forms.IntegerField(min_value=0)

