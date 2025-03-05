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

# ...existing code...

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('nft_list')
    else:
        form = UserCreationForm()
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