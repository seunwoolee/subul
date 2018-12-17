from django import forms
from django.forms import formset_factory, ModelForm

from core.models import Location
from django_select2.forms import Select2Widget
from .models import Egg, EggCode


class EggForm(forms.Form):
    location = forms.ChoiceField(widget=Select2Widget,
                                 choices=list(Location.objects.filter(type='03').values_list('code', 'codeName')
                                              .order_by('code')))
    product = forms.ChoiceField(widget=Select2Widget,
                                choices=list(EggCode.objects.values_list('code', 'codeName')))  # TODO delete_State
    count = forms.IntegerField(min_value=0)
    price = forms.IntegerField(min_value=0)
    memo = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'rows': 2}), required=False
    )
    ymd = forms.CharField(max_length=8, widget=forms.HiddenInput())


EggFormSet = formset_factory(EggForm)