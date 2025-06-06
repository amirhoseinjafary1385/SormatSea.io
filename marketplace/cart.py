from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import NFT

CART_SESSION_ID = 'cart'

def _get_cart(request):

    return request.session.setdefault(CART_SESSION_ID, {})

def add_to_cart(request, nft_id):

    nft = get_object_or_404(NFT, pk=nft_id)
    cart = _get_cart(request)
    str_id = str(nft_id)

    # افزایش تعداد یا مقدار جدید
    cart[str_id] = cart.get(str_id, 0) + 1

    #Save SeSsion

    request.session[setdefault(CART_SESSION_ID, {})] = cart 
    request.session[CART_SESSION_ID] = cart
    request.session.modified = True

    return redirect(request.META.get('HTTP_REFERER', reverse('nft_list')))    

def remove_from_cart(request, nft_id):

    cart = _get_cart(request)
    str_id = str(nft_id)

    if str_id in cart:
        if cart[str_id] > 1:
            cart[str_id] -= 1
        else:
            del cart[str_id]
        request.session[CART_SESSION_ID] = cart
        request.session.modified = True

    return redirect('cart_detail')

    # Your cart is a dict mapping nft_id (as string) to quantity (int).
    # If you want to store more info per item (like price), you could use a dict per item:
    # cart[str_id] = {'quantity': 1, 'price': str(nft.price)}
    # But with your current logic, you only need to store the quantity as you do now.

def cart_detail(request):

    cart = _get_cart(request)
    nft_ids = cart.keys()
    nfts = NFT.objects.filter(id__in=nft_ids)

    cart_items = []
    total_price = 0
    for nft in nfts:
        qty = cart.get(str(nft.id), 0)
        subtotal = nft.price * qty
        total_price += subtotal
        cart_items.append({
            'nft': nft,
            'quantity': qty,
            'subtotal': subtotal,
        })
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'item_count': len(cart_items),
        'cart': cart,
        'nfts': nfts,
        'default': 'cart_detail',
        'title': 'Cart',
        'description': 'Cart',
        'keywords': 'Cart',
        'author': 'Amirhossein',
        'url': 'https://SormatSea.io/cart/',
        'image': 'https://SormatSea.io/static/images/logo.png',
    }
    return render(request, 'marketplace/cart_detail.html', context)
