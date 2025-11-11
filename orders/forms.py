from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from .models import Order


class CheckoutForm(forms.Form):
    customer_name = forms.CharField(
        max_length=100,
        label='Full Name',
        widget=forms.TextInput(attrs={'placeholder': 'John Doe'})
    )
    customer_phone = forms.CharField(
        max_length=20,
        label='Phone Number',
        widget=forms.TextInput(attrs={'placeholder': '+2547XXXXXXXX'})
    )
    customer_address = forms.CharField(
        max_length=255,
        label='Delivery Address (Optional for Pickup)',
        required=False,
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Street, Building, Apartment No.'})
    )

    PAYMENT_CHOICES = Order.DELIVERY_CHOICES
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        label='Payment Method',
        widget=forms.RadioSelect
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('customer_name', css_class='shadow-soft rounded-lg'),
            Field('customer_phone', css_class='shadow-soft rounded-lg'),
            Field('customer_address', css_class='shadow-soft rounded-lg'),
            Field('payment_method', template="orders/partials/payment_radio.html"),
            Submit('submit', 'Place Order (KSh)',
                   css_class='w-full bg-up-primary text-up-light hover:bg-up-secondary transition duration-200 mt-6 rounded-lg')
        )