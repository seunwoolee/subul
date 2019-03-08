from django import forms
from django.forms import formset_factory, ModelForm

from core.models import Location
from django_select2.forms import Select2Widget
from .models import Egg, EggCode


class EggForm(forms.Form):
    EGG_TYPE_CHOICES = (
        ('생산', '생산'),
        ('폐기', '폐기'),
        ('판매', '판매'),
    )

    location = forms.ChoiceField(widget=Select2Widget, choices=Location.objects.none)
    product = forms.ChoiceField(widget=Select2Widget, choices=EggCode.objects.none)
    count = forms.IntegerField(min_value=0)
    amount = forms.IntegerField(min_value=0, required=False)
    price = forms.IntegerField(min_value=0, required=False)
    memo = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'rows': 2}), required=False
    )
    ymd = forms.CharField(max_length=8, widget=forms.HiddenInput(), required=False)
    in_ymd = forms.CharField(max_length=8, widget=forms.HiddenInput())
    type = forms.ChoiceField(choices=EGG_TYPE_CHOICES, required=False)
    fakeYmd = forms.DateField(required=False, widget=forms.DateInput(
        attrs={'type': 'date'}
    ))
    productCode = forms.CharField(widget=forms.HiddenInput(), required=False)
    locationSale = forms.ChoiceField(widget=Select2Widget, required=False,
                                     choices=list(Location.objects.filter(type='07').values_list('code', 'codeName')
                                                  .order_by('code')))
    in_location = forms.CharField(max_length=255, widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(EggForm, self).__init__(*args, **kwargs)
        self.fields['location'] = forms.ChoiceField(widget=Select2Widget,
                                                    choices=[('', '')] + list(
                                                        Location.objects.values_list('code', 'codeName')
                                                        .filter(type='03').filter(delete_state='N').order_by('code')))
        self.fields['product'] = forms.ChoiceField(widget=Select2Widget,
                                                   choices=[('', '')] + list(
                                                       EggCode.objects.values_list('code', 'codeName')))


EggFormSet = formset_factory(EggForm)
