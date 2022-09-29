from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

ORDER_TYPE_CHOICES = [
    ('ret','Return'),
    ('req','Request'),
]

class OrderItemForm(forms.Form):
    # set quantity and order_type
    # other properties are pulled from the request/page
    quantity = forms.IntegerField(
        initial=1,
        widget=widgets.NumberInput(attrs={'class':"form-control"}),
        min_value=1,
        max_value=99
        )
    order_type = forms.ChoiceField(
        choices=ORDER_TYPE_CHOICES,
        widget=widgets.Select(attrs={'class':"dropdown"})
        )

class BasketForm(forms.Form):
        product_name = forms.CharField(
                disabled=True,
                widget=forms.TextInput(attrs={'class':"form-control"})
            )
        quantity = forms.IntegerField(
            widget=widgets.NumberInput(attrs={'class':"form-control"}),
            min_value=0,
            max_value=99
            )
        order_type = forms.ChoiceField(
            choices=ORDER_TYPE_CHOICES,
            widget=widgets.Select(attrs={'class':"dropdown"})
            )
        


class OrderForm(forms.Form):
    #just need to set the date and get address
    pass
