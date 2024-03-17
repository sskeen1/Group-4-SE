from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

TYPES =( 
    ("Buyer", "Buyer"), 
    ("Seller", "Seller"), 
)

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    type = forms.ChoiceField(choices=TYPES)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'type', 'password1', 'password2')