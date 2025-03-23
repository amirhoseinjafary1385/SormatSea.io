from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username")
    firstname = forms.CharField(max_length=50, label="Firstname")
    lastname = forms.CharField(max_length=50, label="Lastname")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    country = forms.CharField(max_length=120, label= "Country | کشور")
    city = forms.CharField(max_length= 120, label= "City | شهر")
    user_id = forms.IntegerField(label= "ID")

