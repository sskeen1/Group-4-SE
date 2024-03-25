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
    
class ListingForm(forms.Form):
    isbn = forms.CharField(max_length=13)
    quantity = forms.IntegerField(initial= 1, min_value=1, max_value=99);
    price = forms.FloatField(initial= 9.99, min_value=1);
    image = forms.ImageField(required=False);

class BookForm(forms.Form):
    title = forms.CharField(max_length=200);
    author = forms.CharField(max_length=200);
    isbn = forms.CharField(max_length=13);
    pages = forms.IntegerField(initial=100, min_value=1);
    rating = forms.FloatField(initial=2.5, min_value=0, max_value=5);
    description = forms.CharField(max_length = 1500, required=False);
