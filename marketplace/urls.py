from django.urls import path
from . import views

urlpatterns = [
    # home / NFT list
    path('', views.nft_list, name='nft_list'),
    # alternative “all NFTs” page
    path('nfts/', views.nfts_view, name='nfts'),
    # single-NFT detail by slug
    path('nft/<slug:slug>/', views.nft_detail, name='nft_detail'),
    # category listing & detail
    path('categories/', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    # user registration
    path('register/', views.register_view, name='register'),
    # payment flow
    path('payment/initiate/<int:nft_id>/', views.initiate_payment, name='initiate_payment'),
    path('payment/verify/', views.verify_payment, name='verify_payment'),
]
