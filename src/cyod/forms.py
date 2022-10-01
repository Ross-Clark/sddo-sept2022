from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from cyod.models import OrderItem

ORDER_TYPE_CHOICES = [
    ('ret','Return'),
    ('req','Request'),
]

class OrderItemProductViewForm(forms.Form):
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

#class BasketForm(forms.Form):
#
#    pk = forms.IntegerField( 
#        widget=forms.HiddenInput()
#    )
#    product_name = forms.CharField(
#            widget=forms.TextInput(attrs={'class':"disabled-form",'readonly': True})
#        )
#    quantity = forms.IntegerField(
#        widget=widgets.NumberInput(attrs={'class':"form-control"}),
#        min_value=0,
#        max_value=99
#        )
#    order_type = forms.ChoiceField(
#        choices=ORDER_TYPE_CHOICES,
#        widget=widgets.Select(attrs={'class':"dropdown"})
#        )
#
#
#    def clean_pk(self):
#        if self.instance: 
#            return self.instance.pk
#        else: 
#            return self.fields['pk']
#
#
#    def clean_product_name(self): 
#        if self.instance: 
#            return self.instance.pk
#        else: 
#            return self.fields['pk']


class BasketForm(forms.ModelForm):

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


    class Meta:
        model = OrderItem
        fields = ['product_name', 'quantity', 'order_type']

class OrderForm(forms.Form):
    #just need to set the date and get address
    pass
