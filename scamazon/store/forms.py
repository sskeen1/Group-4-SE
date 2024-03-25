from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

TYPES =( 
    ("Buyer", "Buyer"), 
    ("Seller", "Seller"), 
)
paytypes = (
("Visa", "Visa"),
("PayPal", "PayPal"),
("Credit", "Credit"),
)

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    type = forms.ChoiceField(choices=TYPES)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'type', 'password1', 'password2')

class CheckoutForm(forms.Form):
    address = forms.CharField(max_length=30)
    paymentType = forms.ChoiceField(choices=paytypes)
    cardNum = forms.CharField(max_length=16)
    CVV = forms.CharField(max_length=3)
    Expiration = forms.DateField()
