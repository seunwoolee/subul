from django import forms
from django.forms import formset_factory

from core.models import Location
from django_select2.forms import Select2Widget
from product.models import ProductCode
from users.models import CustomUser
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

    productCode = forms.CharField(widget=forms.HiddenInput())
    storedLocationCode = forms.CharField(widget=forms.HiddenInput())
    productYmd = forms.CharField(widget=forms.HiddenInput())
    productId = forms.IntegerField(widget=forms.HiddenInput())
    releaseOrder = forms.IntegerField(widget=forms.HiddenInput())
    amount_kg = forms.DecimalField(decimal_places=2, max_digits=19, min_value=0, widget=forms.HiddenInput())
    setProductCode = forms.CharField(widget=forms.HiddenInput())
    totalCount = forms.CharField(widget=forms.HiddenInput(), disabled=True)
    type = forms.ChoiceField(choices=RELEASE_TYPE_CHOICES, widget=Select2Widget)
    location = forms.ChoiceField(widget=Select2Widget, choices=Location.objects.none)
    ymd = forms.CharField(max_length=8)
    amount = forms.DecimalField(decimal_places=2, max_digits=19, min_value=0)
    count = forms.IntegerField(min_value=0)
    price = forms.IntegerField(min_value=0)
    releaseVat = forms.IntegerField(min_value=0)
    orderMemo = forms.CharField( label='', widget=forms.Textarea(attrs={'rows': 2}), required=False)
    memo = forms.CharField( label='', widget=forms.Textarea(attrs={'rows': 2}), required=False)
    fakeYmd = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    location_filter = forms.ChoiceField(widget=Select2Widget, choices=Location.objects.none)
    location_manager = forms.ChoiceField(widget=Select2Widget, choices=CustomUser.objects.none)

    def __init__(self, *args, **kwargs):
        super(ReleaseForm, self).__init__(*args, **kwargs)
        self.fields['location'] = forms.ChoiceField(widget=Select2Widget,
                                                    choices=Location.objects.values_list('code', 'codeName')
                                                    .filter(delete_state='N').order_by('code'))
        self.fields['location_filter'] = forms.ChoiceField(widget=Select2Widget,
                                                    choices=Location.objects.values_list('code', 'codeName')
                                                    .filter(delete_state='N').filter(type='05').order_by('code')
                                                    , required=False)
        self.fields['location_manager'] = forms.ChoiceField(widget=Select2Widget,
                                                    choices=CustomUser.objects.values_list('username', 'first_name')
                                                    .order_by('first_name'), required=False)


class ReleaseLocationForm(forms.Form):
    storedLocation = forms.ChoiceField(choices=list(Location.objects.values_list('code', 'codeName')
                                                     .filter(location_shoppingmall=2).order_by('code')))
