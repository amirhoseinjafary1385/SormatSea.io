from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .models import NFT, Category

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username")
    firstname = forms.CharField(max_length=50, label="Firstname")
    lastname = forms.CharField(max_length=50, label="Lastname")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    country = forms.CharField(max_length=120, label= "Country | کشور")
    city = forms.CharField(max_length= 120, label= "City | شهر")
    user_id = forms.IntegerField(label= "ID")

class LoginForm(AuthenticationForm):
    username = forms.CharField(label = "Username or Email")
    remember_me = forms.BooleanField(required = False, widget = forms.CheckboxInput())

    class Meta:
        fields = ['username', 'password', 'remember_me',]

class NFTForm(forms.ModelForm):

    class Meta:
        model = NFT
        fields = ['title', 'description', 'image', 'category', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'image': forms.FileInput(attrs={'accept': 'image/*'})
        }
        labels = {
            'title': "NFT Title",
            'description': "Description",
            'image': "NFT Image",
            'category': "Category",
            'price': "Price (in ETH)"
        }

