from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import NFT


CART_SESSION_ID = 'cart'


def _get_cart(request):

    return request.session.setdefault(CART_SESSION_ID, {})

def add_to_cart(request, nft_id):

    nft = get_object_or_404(NFT, pk=nft_id)
    cart = _get_cart(request)

