from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .models import NFT, Category
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class BootstrapFormMixining:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            css_classes = widget.attrs.get('class', '').split()

            if isinstance(widget, forms.CheckboxInput):
                css_classes.append('form-check-input')
            elif isinstance(widget, forms.FileInput):
                css_classes.append('form-control')
            widget.attrs['class'] = ' '.join(css_classes).strip()


class RegisterForm(UserCreationForm):

    username = forms.CharField(max_length=150, label="Username")
    firstname = forms.CharField(max_length=50, label="Firstname")
    lastname = forms.CharField(max_length=50, label="Lastname")
    email = forms.EmailField(label="Email", required=True)
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    country = forms.CharField(max_length=120, label= "Country | کشور")
    city = forms.CharField(max_length= 120, label= "City | شهر")
    user_id = forms.IntegerField(label= "ID")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label = "Username or Email")
    remember_me = forms.BooleanField(required = False, widget = forms.CheckboxInput())

    class Meta:
        fields = ['username', 'password', 'remember_me',]

class NFTForm(forms.ModelForm):

    class Meta:
        model = NFT
        fields = ['name', 'description', 'image', 'price_irt', 'price_polygon']

        
        widgets = {
            'price_irt': forms.NumberInput(attrs={'placeholder': 'Price in Toman (IRT)'}),
            'price_polygon': forms.NumberInput(attrs={'placeholder': 'Price in Polygon (MATIC)'}),
        }


        labels = {
            'title': "NFT Title",
            'description': "Description",
            'image': "NFT Image",
            'category': "Category",
            'price': "Price (in ETH)"
        }



