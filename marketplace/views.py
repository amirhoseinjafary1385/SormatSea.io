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
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.decorators.http import require_GET 
from django.utils import timezone
from .cart import cart_detail, add_to_cart, remove_from_cart
from .models import Subcategory
from .models import Category
from django.views import View
from .forms import NFTForm
from .forms import RegisterForm



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form =  RegisterForm()

    return render(request, 'register.html', {'form': form})


def create_nft(request):
    if request.method == 'POST':
        form = NFTForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('nft_list') #whether you want for redirecting
    else:
        form = NFTForm()
    return render(request, 'create_nft.html', {'form': form})



class ProductView(View):
    def get(self, request, subcategory_id=None):
        if subcategory_id:
            subcategory = get_object_or_404(Subcategories, pk=subcategory_id)
            products = subcategory.item.all()
            return render(request, 'products.html', {'subcategory_list': products})
        else:
            category_list = Categories.objects.all()
            return render(request, 'products.html', {'category_list': category_list})    


@require_GET
def home(request):
    """
    Display featured NFTs + trending, top categories, and recommendations.
    """
    now = timezone.now()

    # 1. Featured NFTs: newest 10, only those still within featured_until
    featured_qs = NFT.objects.filter(
        is_featured=True,
        featured_until__gte=now
    ).order_by('-created_at')

    # Annotate how much time is left until the NFT is un-featured
    featured_qs = featured_qs.annotate(
        time_left=ExpressionWrapper(
            F('featured_until') - now,
            output_field=DurationField()
        )
    )
    featured_nfts = featured_qs[:10]
    total_featured = featured_qs.count()

    # 2. Trending NFTs: top 5 by view count (you'll need a 'views' field)
    trending_nfts = NFT.objects.order_by('-views')[:5]

    # 3. Top categories by number of NFTs
    top_categories = (
        Category.objects
        .annotate(num_nfts=Count('nft'))
        .order_by('-num_nfts')[:5]
    )

    # 4. Simple “recommended” NFTs for logged-in users
    recommended_nfts = None
    if request.user.is_authenticated:
        # Example: recommend newest NFTs in categories the user viewed before
        # (You'll need a browsing-history or favorite-category relationship for real logic)
        user_cat_ids = request.user.profile.favored_categories.values_list('id', flat=True)
        recommended_nfts = (
            NFT.objects
            .filter(category__in=user_cat_ids)
            .order_by('-created_at')[:5]
        )

    context = {
        'featured_nfts': featured_nfts,
        'total_featured': total_featured,
        'trending_nfts': trending_nfts,
        'top_categories': top_categories,
        'recommended_nfts': recommended_nfts,
    }

    return render(request, 'marketplace/home.html', context)

@login_required

def initiate_payment(request, nft_id):
    nft = get_object_or_404(NFT, pk = nft_id)

    if request.method == 'post':
        payment_manager = NFTPaymentManager()
        result = payment_manager.process_payment(nft_id, request.user.id)

        if result['success']:
            return redirect(result['payment_url'])
        else:

            message.error(request, f"Payment initiation failed: {result['message']}")
            return redirect('nft_detail', slug=nft.slug)
    
    return render(request, 'marketplace/payment_initiate.html', {'nft': nft})


def verify_payment(request):
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')

    if not authority or not status:
        message.error(request, "Invalid Payment verification requet")
        return redirect('nft_list')

    if status == 'OK':
        payment_manager = NFTPaymentManager()
        transaction = Transaction.objects.get(bank_reference = authority)
        result = payment_manager.verify_payment(authority, transaction.amount)


    if result['success']:
        messages.success(request, "Payment completed successfully!")
        return redirect('nft_detail', slug=result['nft'].slug)
    else:
        messages.error(request, f"Payment verification failed: {result['message']}")
        # This else block handles the case where `result['success']` is False

    messages.warning(request, "Payment was canceled by user")
    return redirect('nft_list')




# class RegisterForm(forms.Form):
#     username = forms.CharField(max_length=150, label="Username")
#     email = forms.EmailField(label="Email")
#     password = forms.CharField(widget=forms.PasswordInput, label="Password")



def category_detail(request, slug):
    
    category  = get_object_or_404(Category, slug= slug)
    nfts = category.nft_set.all()

    return render(request, 'marketplace/category_detail.html', {
        'category': category,
        'nfts': nfts,
    })


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
            login(request, user)
            return redirect('home') # redirect to a Dashboard Page

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
    
    categories = Category.objects.all()
    return render(request, 'marketplace/category_list.html', {'categories': categories})









def nft_detail(request, slug):


    nft = get_object_or_404(NFT, slug=slug)
    related_nfts = NFT.objects.filter(category=nft.category).exclude(id=nft.id)[:4]
    price_history = nft.price_history.all()
    is_owner = request.user.is_autnticated and request.user == nft.owner
    is_featured = nft.is_featured and nft.featured_until > timezone.now()
    is_bidding_open = nft.bidding_end_time > timezone.now()

    context = {
        'nft': nft,
        'related_nfts': related_nfts,
        'price_history': price_history,
        'is_owner': is_owner,
        'is_featured': is_featured,
        'is_bidding_open': is_bidding_open,
    }

    return render(request, 'marketplace/nft_detail.html', {'nft': nft})