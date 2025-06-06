from django.urls import path
from . import views
from . import cart
from .views import ProductView


urlpatterns = [
    path('nft/create/', views.nft_create, name='nft_create'),
    path('create-nft', views.create_nft, name='create-nft'),
    path('products/', ProductView.as_view(), name='product-list'),
    path('products/<int:subcategory_id>/', ProductView.as_view(), name='product-by-subcategory'),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:nft_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:nft_id>/", views.remove_from_cart, name="remove_from_cart"),
    # home / NFT list
    path("", views.nft_list, name="nft_list"),
    # alternative “all NFTs” page
    path("nfts/", views.nfts_view, name="nfts"),
    # single-NFT detail by slug
    path("nft/<slug:slug>/", views.nft_detail, name="nft_detail"),
    # category listing & detail
    path("categories/", views.category_list, name="category_list"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    # user registration
    path("register/", views.register_view, name="register"),
    # payment flow
    path(
        "payment/initiate/<int:nft_id>/",
        views.initiate_payment,
        name="initiate_payment",
    ),
    path("payment/verify/", views.verify_payment, name="verify_payment"),
]
