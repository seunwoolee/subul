from django import forms
from django.forms import formset_factory

from core.models import Location
from django_select2.forms import Select2Widget
from product.models import ProductCode
from .models import Release


class ReleaseForm(forms.Form):
    RELEASE_TYPE_CHOICES = (
        ('판매', '판매'),
        ('샘플', '샘플'),
        ('증정', '증정'),
        ('자손', '자손'),
        ('생산요청', '생산요청'),
        ('반품', '반품'),
        ('이동', '이동'),
        ('미출고품', '미출고품'),
        ('재고조정', '재고조정'),
    )

    # Hidden fields
    productCode = forms.CharField(widget=forms.HiddenInput())
    storedLocationCode = forms.CharField(widget=forms.HiddenInput())
    productYmd = forms.CharField(widget=forms.HiddenInput())
    productId = forms.IntegerField(widget=forms.HiddenInput())
    releaseOrder = forms.IntegerField(widget=forms.HiddenInput())
    amount_kg = forms.DecimalField(decimal_places=2, max_digits=19, min_value=0, widget=forms.HiddenInput())
    setProductCode = forms.CharField(widget=forms.HiddenInput())
    totalCount = forms.CharField(widget=forms.HiddenInput(), disabled=True)

    type = forms.ChoiceField(choices=RELEASE_TYPE_CHOICES, widget=Select2Widget)
    location = forms.ChoiceField(widget=Select2Widget,
                                 choices=list(Location.objects.values_list('code', 'codeName').order_by('code')))
    ymd = forms.CharField(max_length=8)
    amount = forms.DecimalField(decimal_places=2, max_digits=19, min_value=0)
    count = forms.IntegerField(min_value=0)
    price = forms.IntegerField(min_value=0)
    memo = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'rows': 2}), required=False
    )
    fakeYmd = forms.DateField(required=False, widget=forms.DateInput(  # 수정 Modal Ymd
        attrs={'type': 'date'}
    ))


class ReleaseLocationForm(forms.Form):
    storedLocation = forms.ChoiceField(
        choices=list(Location.objects.values_list('code', 'codeName')
                     .filter(location_shoppingmall=2).order_by('code')))
