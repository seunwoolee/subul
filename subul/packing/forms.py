from django import forms
from django.forms import formset_factory, ModelForm

from core.models import Location
from django_select2.forms import Select2Widget
from .models import Packing, PackingCode


class PackingForm(forms.Form):
    PACKING_TYPE_CHOICES = (
        ('생산', '생산'),
        ('폐기', '폐기'),
        ('조정', '조정'),
    )
    type = forms.ChoiceField(choices=PACKING_TYPE_CHOICES, required=False)
    location = forms.ChoiceField(widget=Select2Widget,
                                 choices=[('', '')] + list(
                                     Location.objects.filter(type='01').values_list('code', 'codeName')
                                     .order_by('code')))
    product = forms.ChoiceField(widget=Select2Widget,
                                choices=[('', '')] + list(PackingCode.objects.values_list('code', 'codeName')))
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


PackingFormSet = formset_factory(PackingForm)
