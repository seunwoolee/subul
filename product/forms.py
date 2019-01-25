from django import forms
from django.forms import formset_factory, DecimalField

from core.models import Location
from django_select2.forms import Select2Widget
from .models import ProductCode, ProductEgg, ProductMaster


class MainForm(forms.ModelForm):
    ymd = forms.CharField(max_length=8, widget=forms.HiddenInput())
    total_loss_openEgg = forms.DecimalField(decimal_places=2, max_digits=19, widget=forms.NumberInput(attrs=
    {
        'placeholder': '할란',
        'data-toggle': 'tooltip',
        'data-placement': 'top',
        'title': '할란 로스량 입력'
    }))
    total_loss_insert = forms.DecimalField(decimal_places=2, max_digits=19, widget=forms.NumberInput(attrs=
    {
        'placeholder': '투입',
        'data-toggle': 'tooltip',
        'data-placement': 'top',
        'title': '투입 로스량 입력'
    }))
    total_loss_clean = forms.DecimalField(decimal_places=2, max_digits=19, widget=forms.NumberInput(attrs=
    {
        'placeholder': '살균',
        'data-toggle': 'tooltip',
        'data-placement': 'top',
        'title': '살균 로스량 입력'
    }))
    total_loss_fill = forms.DecimalField(decimal_places=2, max_digits=19, widget=forms.NumberInput(attrs=
    {
        'placeholder': '충진',
        'data-toggle': 'tooltip',
        'data-placement': 'top',
        'title': '충진 로스량 입력'
    }))

    class Meta:
        model = ProductMaster
        fields = ['ymd', 'total_loss_openEgg', 'total_loss_insert', 'total_loss_clean', 'total_loss_fill']


class StepOneForm(forms.Form):
    할란_RawTank전란_01201 = forms.DecimalField(decimal_places=2, max_digits=19, label='Raw Tank 전란', label_suffix='',
                                            help_text='01201',
                                            required=False, min_value=1)
    할란사용_RawTank전란_01201 = forms.DecimalField(decimal_places=2, max_digits=19, label='', required=False, min_value=1)
    메모_RawTank전란_01201_one = forms.CharField(
        label='memo',
        required=False,
        widget=forms.Textarea(attrs={'rows': 1}, )
    )

    할란_RawTank난황_01202 = forms.DecimalField(decimal_places=2, max_digits=19, label='Raw Tank 난황', label_suffix='',
                                            help_text='01202',
                                            required=False, min_value=1)
    할란사용_RawTank난황_01202 = forms.DecimalField(decimal_places=2, max_digits=19, label='', required=False, min_value=1)
    메모_RawTank난황_01202_one = forms.CharField(
        label='memo',
        required=False,
        widget=forms.Textarea(attrs={'rows': 1})
    )

    할란_RawTank난백_01203 = forms.DecimalField(decimal_places=2, max_digits=19, label='Raw Tank 난백', label_suffix='',
                                            help_text='01203',
                                            required=False, min_value=1)
    할란사용_RawTank난백_01203 = forms.DecimalField(decimal_places=2, max_digits=19, label='', required=False, min_value=1)
    메모_RawTank난백_01203_one = forms.CharField(
        label='memo',
        required=False,
        widget=forms.Textarea(attrs={'rows': 1})
    )

    할란_RawTank등급란전란_01207 = forms.DecimalField(decimal_places=2, max_digits=19, label='Raw Tank 등급란전란', label_suffix='',
                                               help_text='01207'
                                               , required=False, min_value=1)
    할란사용_RawTank등급란전란_01207 = forms.DecimalField(decimal_places=2, max_digits=19, label='', required=False, min_value=1)
    메모_RawTank등급란전란_01207_one = forms.CharField(
        label='memo',
        required=False,
        widget=forms.Textarea(attrs={'rows': 1})
    )

    할란_RawTank등급란난황_01208 = forms.DecimalField(decimal_places=2, max_digits=19, label='Raw Tank 등급란난황', label_suffix='',
                                               help_text='01208'
                                               , required=False, min_value=1)
    할란사용_RawTank등급란난황_01208 = forms.DecimalField(decimal_places=2, max_digits=19, label='', required=False, min_value=1)
    메모_RawTank등급란난황_01208_one = forms.CharField(
        label='memo',
        required=False,
        widget=forms.Textarea(attrs={'rows': 1})
    )

    할란_RawTank등급란난백_01209 = forms.DecimalField(decimal_places=2, max_digits=19, label='Raw Tank 등급란난백', label_suffix='',
                                               help_text='01209'
                                               , required=False, min_value=1)
    할란사용_RawTank등급란난백_01209 = forms.DecimalField(decimal_places=2, max_digits=19, label='', required=False, min_value=1)
    메모_RawTank등급란난백_01209_one = forms.CharField(
        label='memo',
        required=False,
        widget=forms.Textarea(attrs={'rows': 1})
    )


class StepTwoForm(forms.Form):
    공정품투입_RawTank전란_01201 = forms.DecimalField(decimal_places=2, max_digits=19, label='Raw Tank 전란', label_suffix='', help_text='01201'
                                               , required=False, min_value=1)
    메모_RawTank전란_01201_two = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'rows': 1})
    )

    공정품투입_RawTank난황_01202 = forms.DecimalField(decimal_places=2, max_digits=19, label='Raw Tank 난황', label_suffix='', help_text='01202'
                                               , required=False, min_value=1)
    메모_RawTank난황_01202_two = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'rows': 1})
    )

    공정품투입_RawTank난백_01203 = forms.DecimalField(decimal_places=2, max_digits=19, label='Raw Tank 난백', label_suffix='', help_text='01203'
                                               , required=False, min_value=1)
    메모_RawTank난백_01203_two = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'rows': 1})
    )

    공정품투입_PastTank전란_01204 = forms.DecimalField(decimal_places=2, max_digits=19, label='Past Tank 전란', label_suffix='', help_text='01204'
                                                , required=False, min_value=1)
    메모_PastTank전란_01204_two = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'rows': 1})
    )

    공정품투입_PastTank난황_01205 = forms.DecimalField(decimal_places=2, max_digits=19, label='Past Tank 난황', label_suffix='', help_text='01205'
                                                , required=False, min_value=1)
    메모_PastTank난황_01205_two = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'rows': 1})
    )

    공정품투입_PastTank난백_01206 = forms.DecimalField(decimal_places=2, max_digits=19, label='Past Tank 난백', label_suffix='', help_text='01206'
                                                , required=False, min_value=1)
    메모_PastTank난백_01206_two = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'rows': 1})
    )

    공정품투입_RawTank등급란전란_01207 = forms.DecimalField(decimal_places=2, max_digits=19, label='Raw Tank 등급란전란', label_suffix='', help_text='01207'
                                                  , required=False, min_value=1)
    메모_RawTank등급란전란_01207_two = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'rows': 1})
    )

    공정품투입_RawTank등급란난황_01208 = forms.DecimalField(decimal_places=2, max_digits=19, label='Raw Tank 등급란난황', label_suffix='', help_text='01208'
                                                  , required=False, min_value=1)
    메모_RawTank등급란난황_01208_two = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'rows': 1})
    )

    공정품투입_RawTank등급란난백_01209 = forms.DecimalField(decimal_places=2, max_digits=19, label='Raw Tank 등급란난백', label_suffix='', help_text='01209'
                                                  , required=False, min_value=1)
    메모_RawTank등급란난백_01209_two = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'rows': 1})
    )


class StepThreeForm(forms.Form):
    공정품발생_RawTank전란_01201 = forms.DecimalField(decimal_places=2, max_digits=19, label='Raw Tank 전란', label_suffix='', help_text='01201'
                                               , required=False, min_value=1)
    메모_RawTank전란_01201_three = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'rows': 1})
    )

    공정품발생_RawTank난황_01202 = forms.DecimalField(decimal_places=2, max_digits=19, label='Raw Tank 난황', label_suffix='', help_text='01202'
                                               , required=False, min_value=1)
    메모_RawTank난황_01202_three = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'rows': 1})
    )

    공정품발생_RawTank난백_01203 = forms.DecimalField(decimal_places=2, max_digits=19, label='Raw Tank 난백', label_suffix='', help_text='01203'
                                               , required=False, min_value=1)
    메모_RawTank난백_01203_three = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'rows': 1})
    )

    공정품발생_PastTank전란_01204 = forms.DecimalField(decimal_places=2, max_digits=19, label='Past Tank 전란', label_suffix='', help_text='01204'
                                                , required=False, min_value=1)
    메모_PastTank전란_01204_three = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'rows': 1})
    )

    공정품발생_PastTank난황_01205 = forms.DecimalField(decimal_places=2, max_digits=19, label='Past Tank 난황', label_suffix='', help_text='01205'
                                                , required=False, min_value=1)
    메모_PastTank난황_01205_three = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'rows': 1})
    )

    공정품발생_PastTank난백_01206 = forms.DecimalField(decimal_places=2, max_digits=19, label='Past Tank 난백', label_suffix='', help_text='01206'
                                                , required=False, min_value=1)
    메모_PastTank난백_01206_three = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'rows': 1})
    )

    공정품발생_RawTank등급란전란_01207 = forms.DecimalField(decimal_places=2, max_digits=19, label='Raw Tank 등급란전란', label_suffix='', help_text='01207'
                                                  , required=False, min_value=1)
    메모_RawTank등급란전란_01207_three = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'rows': 1})
    )

    공정품발생_RawTank등급란난황_01208 = forms.DecimalField(decimal_places=2, max_digits=19, label='Raw Tank 등급란난황', label_suffix='', help_text='01208'
                                                  , required=False, min_value=1)
    메모_RawTank등급란난황_01208_three = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'rows': 1})
    )

    공정품발생_RawTank등급란난백_01209 = forms.DecimalField(decimal_places=2, max_digits=19, label='Raw Tank 등급란난백', label_suffix='', help_text='01209'
                                                  , required=False, min_value=1)
    메모_RawTank등급란난백_01209_three = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'rows': 1})
    )


class StepFourForm(forms.Form):
    product = forms.ChoiceField(widget=Select2Widget,
                                choices=list(ProductCode.objects.values_list('code', 'codeName')
                                             .filter(delete_state='N').order_by('code')), required=False)
    amount = forms.DecimalField(decimal_places=2, max_digits=19, min_value=0)
    amount_kg = forms.DecimalField(decimal_places=2, max_digits=19, min_value=0, widget=forms.HiddenInput())
    count = forms.IntegerField(min_value=0)
    memo = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'rows': 2}), required=False
    )


StepFourFormSet = formset_factory(StepFourForm)


class ProductOEMForm(forms.Form):
    product = forms.ChoiceField(widget=Select2Widget,
                                choices=[('', '')] + list(ProductCode.objects.values_list('code', 'codeName')
                                                          .filter(delete_state='N').filter(oem='Y').order_by('code')))
    location = forms.ChoiceField(widget=Select2Widget,
                                 choices=[('', '')] + list(Location.objects.values_list('code', 'codeName')
                                     .filter(delete_state='N').filter(type='09').order_by(
                                     'code')))
    count = forms.IntegerField(min_value=0)
    purchaseSupplyPrice = forms.IntegerField(min_value=0)
    purchaseVat = forms.IntegerField(min_value=0, required=False)
    memo = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'rows': 2}), required=False
    )
    fakeYmd = forms.DateField(required=False, widget=forms.DateInput(
        attrs={'type': 'date'}
    ))
    fakePurchaseYmd = forms.DateField(required=False, widget=forms.DateInput(
        attrs={'type': 'date'}
    ))
    ymd = forms.CharField(max_length=8, widget=forms.HiddenInput())
    purchaseYmd = forms.CharField(max_length=8, widget=forms.HiddenInput())


ProductOEMFormSet = formset_factory(ProductOEMForm)
