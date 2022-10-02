from django import forms
from django.core.validators import RegexValidator
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from cyod.models import OrderItem, Order

ORDER_TYPE_CHOICES = [
    ("ret", "Return"),
    ("req", "Request"),
]


class OrderItemProductViewForm(forms.Form):
    # set quantity and order_type
    # other properties are pulled from the request/page
    quantity = forms.IntegerField(
        initial=1,
        widget=widgets.NumberInput(attrs={"class": "form-control"}),
        min_value=1,
        max_value=99,
    )
    order_type = forms.ChoiceField(
        choices=ORDER_TYPE_CHOICES, widget=widgets.Select(attrs={"class": "dropdown"})
    )


class BasketForm(forms.ModelForm):

    product_name = forms.CharField(
        disabled=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )

    quantity = forms.IntegerField(
        widget=widgets.NumberInput(attrs={"class": "form-control"}),
        min_value=1,
        max_value=99,
    )

    order_type = forms.ChoiceField(
        choices=ORDER_TYPE_CHOICES, widget=widgets.Select(attrs={"class": "dropdown"})
    )

    class Meta:
        model = OrderItem
        fields = ["product_name", "quantity", "order_type"]


class OrderForm(forms.ModelForm):

    address1 = forms.CharField(
        label="Address 1", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    address2 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Address 2",
        help_text="Not required",
    )
    address3 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Address 3",
        help_text="Not required",
    )
    town = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Town",
    )
    # postcode regex from govuk
    # https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/488478/Bulk_Data_Transfer_-_additional_validation_valid_from_12_November_2015.pdf
    # pg 6

    postCodeRegex = r"([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9][A-Za-z]?))))\s?[0-9][A-Za-z]{2})"

    postcode = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[
            RegexValidator(regex=postCodeRegex, message="Please enter a valid postcode")
        ],
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[
            RegexValidator(
                # simple regex for phone numbers with plus space and dashes in
                # between 9 and 10 numbers
                regex=r"^\s*\+?\s*([0-9][\s-]*){9,15}$",
                message="Please enter a valid phonenumber",
            )
        ],
    )
    justification = forms.CharField(
        required=False,
        help_text="Max 500 chars. Not required",
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Order
        fields = [
            "address1",
            "address2",
            "address3",
            "town",
            "postcode",
            "phone",
            "justification",
        ]
