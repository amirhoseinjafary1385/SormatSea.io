
from django.contrib import admin
from .models import Category, NFT
#from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


#@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email' , 'country',  'city')
    list_display_links =  ('username', 'email')
    list_filter = (
        'is_staff', 'is_active', 'country', 'city', 'groups'
    )

    search_fields = (
        'username', 'email', 'first_name', 'last_name',
        'country', 'city'
    )

    ordering = ('username',)
    save_on_top = True
    
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Location Info', {
            'classes': ('collapse',),
            'fields': ('country', 'city')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    # Fields layout on the “add user” page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'first_name', 'last_name',
                'country', 'city', 'password1', 'password2'
            ),
        }),
    )

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

filter_horizontal = ('groups', 'user_permissions',)


