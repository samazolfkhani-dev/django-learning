from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username' , 'email' , 'phone' , 'job' , 'date_of_birth']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information' , {'fields': ('date_of_birth', 'bio' , 'job' , 'phone' , 'photo')}),
    )