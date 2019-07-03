from django import forms
from django.forms import formset_factory, ModelForm

from core.models import Location
from django_select2.forms import Select2Widget
from product.models import ProductCode
from .models import Packing, PackingCode


class PackingForm(forms.Form):
    PACKING_TYPE_CHOICES = (
        ('생산', '생산'),
        ('폐기', '폐기'),
        ('조정', '조정'),
    )
    type = forms.ChoiceField(choices=PACKING_TYPE_CHOICES, required=False)
    location = forms.ChoiceField(widget=Select2Widget, choices=Location.objects.none)
    product = forms.ChoiceField(widget=Select2Widget, choices=PackingCode.objects.none)
    code = forms.CharField(widget=forms.HiddenInput(), required=False)
    count = forms.IntegerField(min_value=0)
    price = forms.IntegerField(min_value=0)
    memo = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'rows': 2}), required=False
    )
    ymd = forms.CharField(max_length=8, widget=forms.HiddenInput())
    fakeYmd = forms.DateField(required=False, widget=forms.DateInput(
        attrs={'type': 'date'}
    ))

    def __init__(self, *args, **kwargs):
        super(PackingForm, self).__init__(*args, **kwargs)
        self.fields['location'] = forms.ChoiceField(widget=Select2Widget,
                                                    choices=[('', '')] + list(
                                                        Location.objects.values_list('code', 'codeName')
                                                            .filter(type='01').filter(delete_state='N').order_by(
                                                            'code')))
        self.fields['product'] = forms.ChoiceField(widget=Select2Widget,
                                                   choices=[('', '')] + list(
                                                       PackingCode.objects.values_list('code', 'codeName')))


PackingFormSet = formset_factory(PackingForm)


class AutoPackingForm(forms.Form):
    product = forms.ChoiceField(widget=Select2Widget, choices=ProductCode.objects.none)
    packing = forms.ChoiceField(widget=Select2Widget, choices=PackingCode.objects.none)
    count = forms.IntegerField(min_value=0, label='개수')
    productCode = forms.CharField(widget=forms.HiddenInput())  # 생성 form
    packingCode = forms.CharField(widget=forms.HiddenInput())  # 생성 form

    def __init__(self, *args, **kwargs):
        super(AutoPackingForm, self).__init__(*args, **kwargs)
        self.fields['product'] = forms.ChoiceField(widget=Select2Widget,
                                                   choices=[('', '')] + list(
                                                       ProductCode.objects.values_list('id', 'codeName')
                                                           .filter(delete_state='N')))
        self.fields['packing'] = forms.ChoiceField(widget=Select2Widget,
                                                   choices=[('', '')] + list(
                                                       PackingCode.objects.values_list('id', 'codeName')
                                                           .filter(delete_state='N')))
