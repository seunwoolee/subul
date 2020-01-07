from django import forms
from django.db.models import F, Value
from django.forms import formset_factory
from django.db.models.functions import Concat

from core.models import Location
from django_select2.forms import Select2Widget
from .models import ProductCode, ProductEgg, ProductMaster, SetProductCode


class ProductUnitPricesForm(forms.Form):
    location = forms.ChoiceField(widget=Select2Widget, choices=Location.objects.none)
    product = forms.ChoiceField(widget=Select2Widget, choices=ProductCode.objects.none)
    price = forms.DecimalField(decimal_places=1, max_digits=19, min_value=0)
    specialPrice = forms.DecimalField(decimal_places=1, max_digits=19, min_value=0, required=False)
    locationCode = forms.CharField(widget=forms.HiddenInput())  # 생성 form
    productCode = forms.CharField(widget=forms.HiddenInput())  # 생성 form

    def __init__(self, *args, **kwargs):
        super(ProductUnitPricesForm, self).__init__(*args, **kwargs)
        self.fields['location'] = forms.ChoiceField(widget=Select2Widget,
                                                    choices=[('', '')] + list(
                                                        Location.objects.values_list('code', 'codeName')
                                                        .filter(type='05').filter(delete_state='N').order_by('code')))
        self.fields['product'] = forms.ChoiceField(widget=Select2Widget,
                                                   choices=[('', '')] + list(
                                                       ProductCode.objects.values_list('code', 'codeName')
                                                       .filter(delete_state='N').order_by('code')))


class SetProductMatchForm(forms.Form):
    location = forms.ChoiceField(widget=Select2Widget, choices=Location.objects.none)
    setProduct = forms.ChoiceField(widget=Select2Widget, choices=SetProductCode.objects.none)
    product = forms.ChoiceField(widget=Select2Widget, choices=ProductCode.objects.none)
    price = forms.DecimalField(decimal_places=1, max_digits=19, min_value=0)
    count = forms.IntegerField(min_value=0)
    locationCode = forms.CharField(widget=forms.HiddenInput())  # 생성 form
    setProductCode = forms.CharField(widget=forms.HiddenInput())  # 생성 form

    def __init__(self, *args, **kwargs):
        super(SetProductMatchForm, self).__init__(*args, **kwargs)
        setProduct = [('', '')] + list(SetProductCode.objects\
            .annotate(full_codename=Concat(Value('['), F('location__codeName'), Value(']'), F('codeName')))\
            .values_list('code', 'full_codename'))

        self.fields['location'] = forms.ChoiceField(widget=Select2Widget,
                                                    choices=[('', '')] + list(
                                                        Location.objects.values_list('code', 'codeName')
                                                        .filter(type='05').filter(delete_state='N').order_by('code')))
        self.fields['product'] = forms.ChoiceField(widget=Select2Widget,
                                                   choices=[('', '')] + list(
                                                       ProductCode.objects.values_list('code', 'codeName')
                                                       .filter(delete_state='N').order_by('code')))
        self.fields['setProduct'] = forms.ChoiceField(widget=Select2Widget, choices=setProduct)


class ProductCodeForm(forms.ModelForm):
    class Meta:
        model = ProductCode
        fields = ('expiration', 'calculation')
        labels = {
            'expiration': '유통기한',
            'calculation': '계산'
        }
