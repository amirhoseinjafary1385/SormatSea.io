from django.urls import path
from . import views

urlpatterns = [
    path('', views.nft_list, name='nft_list'),
    path('category/<int:id>/', views.category_detail, name='category_detail'),
    path('categories', views.category_list, name='category_list'),
    path('nft/<slug:slug>/', views.nft_detail, name='nft_detail'),
    path('nfts', views.nfts_view, name='nfts'),
    path('register', views.register_view, name='register'),  # Added register URL pattern
    path('category/<slug:slug>/', views.category_detail, name = 'category_detail'),
]
