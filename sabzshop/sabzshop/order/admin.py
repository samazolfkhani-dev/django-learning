from django.contrib import admin
from .models import *

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id' , 'first_name' , 'last_name' , 'phone' , 'address' , 'postal_code' , 'provinance' ,
                    'city' , 'paid' , 'created' , 'updated']
    inlines = [OrderItemInline]
    list_filter = ['paid' , 'created' , 'updated']