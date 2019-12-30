from django import forms
from .models import Location


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
