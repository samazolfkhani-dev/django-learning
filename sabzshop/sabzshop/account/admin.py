from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ShopUser
from .forms import ShopUserCreationForm , ShopUserChangeForm
# Register your models here.

@admin.register(ShopUser)
class ShopUserAdmin(UserAdmin):
    ordering = ['phone']
    add_form = ShopUserCreationForm
    form = ShopUserChangeForm
    model = ShopUser
    list_display = ['phone', 'first_name', 'last_name', 'is_staff' , 'is_active']
    fieldsets = (
        (None , {'fields' : ('phone' , 'password')}),
        ('Personal fields' , {'fields' : ('first_name' , 'last_name' , 'address')}),
        ('Permission' , {'fields' : ('is_active' , 'is_staff' , 'is_superuser')}),
        ('Importatnt Date' , {'fields' : ('date_joined' , 'last_login')}),
    )

    add_fieldsets = (
        (None , {'fields' : ('phone' , 'password')}),
        ('Personal fields' , {'fields' : ('first_name' , 'last_name' , 'address')}),
        ('Permission' , {'fields' : ('is_active' , 'is_staff' , 'is_superuser')}),
        ('Importatnt Date' , {'fields' : ('date_joined' , 'last_login')}),
    )