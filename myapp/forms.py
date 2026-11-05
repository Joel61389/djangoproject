from django import forms

from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("customer_name", "email", "delivery_address")
        widgets = {
            "customer_name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "delivery_address": forms.Textarea(
                attrs={"autocomplete": "street-address", "rows": 3}
            ),
        }
