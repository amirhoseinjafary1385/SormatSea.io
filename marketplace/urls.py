from django.urls import path
from . import views
from marketplace import views

#debug
#print(dir(marketplace.views))


urlpatterns = [
    path('payment/initiate/', views.initiate_payment, name='initiate_payment'),
    path('payment/verify/', views.verify_payment, name='verify_payment'),
    path('', views.nft_list, name='nft_list'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('categories', views.category_list, name='category_list'),
    path('nft/<slug:slug>/', views.nft_detail, name='nft_detail'),
    path('nfts', views.nfts_view, name='nfts'),
    path('register', views.register_view, name='register'),  # Added register URL pattern
    path('category/<slug:slug>/', views.category_detail, name = 'category_detail'),
]
