from django import forms

from eggs.models import EggOrder


class EggOrderForm(forms.ModelForm):

    class Meta:
        model = EggOrder
        fields = ('realCount', 'site_memo')


class EggOrderModifyForm(forms.ModelForm):

    class Meta:
        model = EggOrder
        fields = ('realCount', 'orderCount', 'memo', 'site_memo')
