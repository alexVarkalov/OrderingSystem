from django import forms


class OrderForm(forms.Form):
    product = forms.CharField(max_length=30)
    customer = forms.CharField(max_length=40)
    email = forms.EmailField()
    paid_BYR = forms.IntegerField(min_value=100)
    paid_BYN = forms.FloatField(min_value=0.01)
    comment = forms.CharField(max_length=300)
