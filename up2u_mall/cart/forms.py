from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]


class CartAddProductForm(forms.Form):
    """
    使用TypedChoiceField进行数量选择，并通过 coerce=int进行整数转换.
    """
    quantity = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int,
                                label='数量')
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
