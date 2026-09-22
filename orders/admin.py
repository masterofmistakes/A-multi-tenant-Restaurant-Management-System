from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'restaurant', 'client', 'waiter', 'table_number', 'order_status', 'total_price', 'payment_method', 'payment_status', 'created_at', 'updated_at')
    list_filter = ('restaurant', 'waiter', 'client' )
    search_fields = ('restaurant', 'client', 'waiter')
