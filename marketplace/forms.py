from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length= 100, required = True)
    last_name = forms.CharField(max_length= 100, required = True)
    email = forms.EmailField(required= True)
    country = forms.CharField(max_length = 100, required= True)
    city = forms.CharField(max_length= 100, required= True)
    
    
    class Meta:
        
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'country', 'city', 'password1', 'password2']