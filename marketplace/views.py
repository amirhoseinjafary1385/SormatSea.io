from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
#from .forms import RegistrationForm  
from django.contrib.auth.forms import AuthenticationForm
#from .models import CustomUser
from .models import NFT, Category
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from django import forms
from django.contrib.auth.models import User
from .forms import RegisterForm



# class RegisterForm(forms.Form):
#     username = forms.CharField(max_length=150, label="Username")
#     email = forms.EmailField(label="Email")
#     password = forms.CharField(widget=forms.PasswordInput, label="Password")



def category_detail(request, slug):
    category  = get_object_or_404(Category, slug= slug)
    return render(request, 'marketplace/category_detail.html', {'category': category})


def nfts_view(request):
    return render(request, 'marketplace/nfts.html')


# ...existing code...

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Save the user to the database
            User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            return HttpResponse("Registration successful!")
    else:
        form = RegisterForm()

    return render(request, 'marketplace/register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=  request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('nft_list')
    else:
        form = AuthenticationForm()
    return render(request, 'marketplace/login.html', {'form': form})
    


@login_required
def user_logout(request):
    logout(request)
    return redirect('nft_list')
               

def nft_list(request):
    nfts = NFT.objects.all()
    return render(request, 'marketplace/nft_list.html', {'nfts': nfts})

def category_list(request):
    
    """
    Display a list of all available categories.
    """
    categories = Category.objects.all()
    return render(request, 'marketplace/category_list.html', {'categories': categories})

def nft_detail(request, slug):
    """
    Display the details of a specific NFT.
    """
    nft = get_object_or_404(NFT, slug=slug)
    
    return render(request, 'marketplace/nft_detail.html', {'nft': nft})