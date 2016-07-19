from django import forms


class OrderForm(forms.Form):
    product = forms.CharField(max_length=30)
    customer = forms.CharField(max_length=40)
    email = forms.EmailField()
    paid_BYR = forms.IntegerField(min_value=100, required=False, label='Paid BYR')
    paid_BYN = forms.FloatField(min_value=0.01, required=False, label='Paid BYN')
    comment = forms.CharField(max_length=300, required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        paid_BYR = cleaned_data.get('paid_BYR')
        paid_BYN = cleaned_data.get('paid_BYN')
        if not (paid_BYR or paid_BYN):
            raise forms.ValidationError('BYR and BYN paid can not be blank together')
        return cleaned_data