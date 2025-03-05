from django.urls import path
from . import views

urlpatterns = [
    path('', views.nft_list, name='nft_list'),
    path('categories/', views.category_list, name='category_list'),
    path('nft/<slug:slug>/', views.nft_detail, name='nft_detail'),
    path('register/', views.register, name='register'),  # Added register URL pattern
]
