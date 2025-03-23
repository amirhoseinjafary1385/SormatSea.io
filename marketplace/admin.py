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


#admin.site.register(CustomUser ,CustomUserAdmin)
admin.site.register(Category)
admin.site.register(NFT, NFTAdmin) 
