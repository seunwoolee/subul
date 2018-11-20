from django import forms
from django.forms import formset_factory

from core.models import Location
from django_select2.forms import Select2Widget
from product.models import ProductCode
from .models import Order




class OrderForm(forms.Form):
    ORDER_TYPE_CHOICES = (
        ('판매', '판매'),
        ('샘플', '샘플'),
        ('증정', '증정'),
        ('자손', '자손'),
        ('생산요청', '생산요청'),
    )

    SET_TYPE_CHOICES = (
        ('일반', '일반'),
        ('패키지', '패키지'),
    )

    SPECIALTAG_TYPE_CHOICES = (
        ('일반', '일반'),
        ('특인가', '특인가'),
    )

    set = forms.ChoiceField(choices=SET_TYPE_CHOICES)
    type = forms.ChoiceField(choices=ORDER_TYPE_CHOICES)
    location = forms.ChoiceField(widget=Select2Widget,
                                 choices=list(Location.objects.values_list('code', 'codeName').order_by('code')),
                                 required=False)
    product = forms.ChoiceField(choices=list(ProductCode.objects.values_list('code', 'codeName'))) # TODO delete_State
    amount = forms.FloatField(min_value=0)
    amount_kg = forms.FloatField(min_value=0, widget=forms.HiddenInput())
    count = forms.IntegerField(min_value=0)
    price = forms.IntegerField(min_value=0)
    memo = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'rows': 2}), required=False
    )
    ymd = forms.CharField(max_length=8, widget=forms.HiddenInput())
    package = forms.CharField(widget=forms.HiddenInput(), required=False)
    specialTag = forms.ChoiceField(choices=SPECIALTAG_TYPE_CHOICES)
OrderFormSet = formset_factory(OrderForm)