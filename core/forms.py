from django import forms
from django.db.models import Q
from django.forms import formset_factory

from .models import Location, WEEK_DAY_CHOICES
from django_select2.forms import Select2Widget
from product.models import ProductCode
from users.models import CustomUser


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('codeName', 'type', 'location_address', 'location_phone', 'location_companyNumber', 'location_owner',
                  'location_character', 'location_manager', 'location_address_category')
        labels = {
            'codeName': '거래처명',
            'type': '거래처 구분',
            'location_address': '주소',
            'location_phone': '전화번호',
            'location_companyNumber': '사업자 번호',
            'location_owner': '대표자명',
            'location_character': '분류',
            'location_manager': '담당자',
            'location_address_category': '지역분류'
        }


class OrderTimeForm(forms.Form):
    company = forms.ChoiceField(widget=Select2Widget, choices=CustomUser.objects.none)
    weekday = forms.ChoiceField(choices=WEEK_DAY_CHOICES)
    start = forms.CharField()
    end = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(OrderTimeForm, self).__init__(*args, **kwargs)
        self.fields['company'] = forms.ChoiceField(widget=Select2Widget,
                                                   choices=CustomUser.objects.values_list('id', 'username')
                                                   .filter(Q(last_name='업체'), Q(is_active=True)).order_by('username'),
                                                   required=False)


OrderTimeFormSet = formset_factory(OrderTimeForm)
