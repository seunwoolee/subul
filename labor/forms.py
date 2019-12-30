from django import forms

from core.models import Location
from eggs.models import EggOrder
from release.models import Car


class EggOrderForm(forms.ModelForm):
    class Meta:
        model = EggOrder
        fields = ('realCount', 'site_memo')


class EggOrderModifyForm(forms.ModelForm):
    class Meta:
        model = EggOrder
        fields = ('realCount', 'orderCount', 'memo', 'site_memo')


class ReleaseLabor(forms.Form):
    location = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=Location.objects.none())
    car = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=Car.objects.none())

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.fields['location'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'form-control'}),
            choices=[('', '')] +
                    list(Location.objects.values_list('location_address_category',
                                                      'location_address_category')
                         .distinct('location_address_category').order_by('location_address_category')))
        self.fields['car'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': 'form-control'}),
            choices=[('', '')] +
                    list(Car.objects.values_list('id', 'car_number')
                         .distinct('car_number').order_by('car_number')))
