
from django.contrib import admin
from .models import Category, NFT
#from .models import CustomUser
from django.contrib.auth.admin import UserAdmin



class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email' , 'country',  'city')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields' : ('country', 'city')}),
    )

class NFTAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'owner', 'price', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description') # Searchable fields

#admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(NFT, NFTAdmin) 
