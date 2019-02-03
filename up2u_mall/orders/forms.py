from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'placeholder': '收货人姓名',
             'class': "form-control"
             }
        ),
        )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'placeholder': '手机号码',
             'class': "form-control"
             }
        ),
        )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'placeholder': '邮箱',
             'class': "form-control"
             }
        ),
        )
    city = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'placeholder': '城市',
             'class': "form-control"
             }
        ),
        )
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'placeholder': '地址',
             'class': "form-control"
             }
        ),
        )
    class Meta:
        model = Order
        fields = ['name', 'phone', 'email', 'city', 'address']
