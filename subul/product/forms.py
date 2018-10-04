from django import forms
from django.forms import formset_factory
from django_select2.forms import Select2Widget

class StepOneForm(forms.Form):
    RawTank_전란할란 = forms.IntegerField(label='Raw Tank 전란',label_suffix='' ,help_text='01201')
    RawTank_전란할란사용 = forms.IntegerField(label='')
    RawTank_전란할란메모 = forms.CharField(
                    label='',
                    widget=forms.Textarea(attrs={'rows':1})
                    )

    RawTank_난황할란 = forms.IntegerField(label='Raw Tank 난황',label_suffix='' ,help_text='01202')
    RawTank_난황할란사용 = forms.IntegerField(label='')
    RawTank_난황할란메모 = forms.CharField(
                    label='',
                    widget=forms.Textarea(attrs={'rows':1})
                    )

    RawTank_난백할란 = forms.IntegerField(label='Raw Tank 난백',label_suffix='' ,help_text='01203')
    RawTank_난백할란사용 = forms.IntegerField(label='')
    RawTank_난백할란메모 = forms.CharField(
                    label='',
                    widget=forms.Textarea(attrs={'rows':1})
                    )

    RawTank_등급란전란할란 = forms.IntegerField(label='Raw Tank 등급란전란',label_suffix='' ,help_text='01207')
    RawTank_등급란전란할란사용 = forms.IntegerField(label='')
    RawTank_등급란전란할란메모 = forms.CharField(
                    label='',
                    widget=forms.Textarea(attrs={'rows':1})
                    )

    RawTank_등급란난황할란 = forms.IntegerField(label='Raw Tank 등급란난황',label_suffix='' ,help_text='01208')
    RawTank_등급란난황할란사용 = forms.IntegerField(label='')
    RawTank_등급란난황할란메모 = forms.CharField(
                    label='',
                    widget=forms.Textarea(attrs={'rows':1})
                    )

    RawTank_등급란난백할란 = forms.IntegerField(label='Raw Tank 등급란난백',label_suffix='' ,help_text='01209')
    RawTank_등급란난백할란사용 = forms.IntegerField(label='')
    RawTank_등급란난백할란메모 = forms.CharField(
                    label='',
                    widget=forms.Textarea(attrs={'rows':1})
                    )


class StepTwoForm(forms.Form):
    RawTank_전란공정품투입 = forms.IntegerField(label='Raw Tank 전란',label_suffix='' ,help_text='01201')
    RawTank_전란공정품투입메모 = forms.CharField(
                    label='',
                    widget=forms.Textarea(attrs={'rows':1})
                    )

    RawTank_난황공정품투입 = forms.IntegerField(label='Raw Tank 난황',label_suffix='' ,help_text='01202')
    RawTank_난황공정품투입메모 = forms.CharField(
                    label='',
                    widget=forms.Textarea(attrs={'rows':1})
                    )

    RawTank_난백공정품투입 = forms.IntegerField(label='Raw Tank 난황',label_suffix='' ,help_text='01203')
    RawTank_난백공정품투입메모 = forms.CharField(
                    label='',
                    widget=forms.Textarea(attrs={'rows':1})
                    )

    PastTank_전란공정품투입 = forms.IntegerField(label='Past Tank 전란',label_suffix='' ,help_text='01204')
    PastTank_전란공정품투입메모 = forms.CharField(
                    label='',
                    widget=forms.Textarea(attrs={'rows':1})
                    )

    PastTank_난황공정품투입 = forms.IntegerField(label='Past Tank 난황',label_suffix='' ,help_text='01205')
    PastTank_난황공정품투입메모 = forms.CharField(
                    label='',
                    widget=forms.Textarea(attrs={'rows':1})
                    )

    PastTank_난백공정품투입 = forms.IntegerField(label='Past Tank 난황',label_suffix='' ,help_text='01206')
    PastTank_난백공정품투입메모 = forms.CharField(
                    label='',
                    widget=forms.Textarea(attrs={'rows':1})
                    )

    RawTank_등급란전란공정품투입 = forms.IntegerField(label='Raw Tank 등급란전란',label_suffix='' ,help_text='01207')
    RawTank_등급란전란공정품투입메모 = forms.CharField(
                    label='',
                    widget=forms.Textarea(attrs={'rows':1})
                    )

    RawTank_등급란난황공정품투입 = forms.IntegerField(label='Raw Tank 등급란난황',label_suffix='' ,help_text='01208')
    RawTank_등급란난황공정품투입메모 = forms.CharField(
                    label='',
                    widget=forms.Textarea(attrs={'rows':1})
                    )

    RawTank_등급란난백공정품투입 = forms.IntegerField(label='Raw Tank 등급란난백',label_suffix='' ,help_text='01209')
    RawTank_등급란난백공정품투입메모 = forms.CharField(
                    label='',
                    widget=forms.Textarea(attrs={'rows':1})
                    )


class StepThreeForm(forms.Form):
    RawTank_전란공정품발생 = forms.IntegerField(label='Raw Tank 전란',label_suffix='' ,help_text='01201')
    RawTank_전란공정품발생메모 = forms.CharField(
                    label='',
                    widget=forms.Textarea(attrs={'rows':1})
                    )

    RawTank_난황공정품발생 = forms.IntegerField(label='Raw Tank 난황',label_suffix='' ,help_text='01202')
    RawTank_난황공정품발생메모 = forms.CharField(
                    label='',
                    widget=forms.Textarea(attrs={'rows':1})
                    )

    RawTank_난백공정품발생 = forms.IntegerField(label='Raw Tank 난황',label_suffix='' ,help_text='01203')
    RawTank_난백공정품발생메모 = forms.CharField(
                    label='',
                    widget=forms.Textarea(attrs={'rows':1})
                    )

    PastTank_전란공정품발생 = forms.IntegerField(label='Past Tank 전란',label_suffix='' ,help_text='01204')
    PastTank_전란공정품발생메모 = forms.CharField(
                    label='',
                    widget=forms.Textarea(attrs={'rows':1})
                    )

    PastTank_난황공정품발생 = forms.IntegerField(label='Past Tank 난황',label_suffix='' ,help_text='01205')
    PastTank_난황공정품발생메모 = forms.CharField(
                    label='',
                    widget=forms.Textarea(attrs={'rows':1})
                    )

    PastTank_난백공정품발생 = forms.IntegerField(label='Past Tank 난황',label_suffix='' ,help_text='01206')
    PastTank_난백공정품발생메모 = forms.CharField(
                    label='',
                    widget=forms.Textarea(attrs={'rows':1})
                    )

    RawTank_등급란전란공정품발생 = forms.IntegerField(label='Raw Tank 등급란전란',label_suffix='' ,help_text='01207')
    RawTank_등급란전란공정품발생메모 = forms.CharField(
                    label='',
                    widget=forms.Textarea(attrs={'rows':1})
                    )

    RawTank_등급란난황공정품발생 = forms.IntegerField(label='Raw Tank 등급란난황',label_suffix='' ,help_text='01208')
    RawTank_등급란난황공정품발생메모 = forms.CharField(
                    label='',
                    widget=forms.Textarea(attrs={'rows':1})
                    )

    RawTank_등급란난백공정품발생 = forms.IntegerField(label='Raw Tank 등급란난백',label_suffix='' ,help_text='01209')
    RawTank_등급란난백공정품발생메모 = forms.CharField(
                    label='',
                    widget=forms.Textarea(attrs={'rows':1})
                    )


class StepFourForm(forms.Form):
    NUMBER_CHOICES = [
        (1, 'One'),
        (2, 'Two'),
        (3, 'asdfasdf'),
        (4, 'Four'),
    ]
    product = forms.ChoiceField(widget=Select2Widget, choices=NUMBER_CHOICES, required=False)
    amount = forms.IntegerField()
    count= forms.IntegerField()
    memo = forms.CharField(
                    label='',
                    widget=forms.Textarea(attrs={'rows':2})
                    )
StepFourFormSet = formset_factory(StepFourForm)


class Select2WidgetForm(forms.Form):
    NUMBER_CHOICES = [
        (1, 'One'),
        (2, 'Two'),
        (3, 'Three'),
        (4, 'Four'),
    ]
    number = forms.ChoiceField(widget=Select2Widget, choices=NUMBER_CHOICES, required=False)