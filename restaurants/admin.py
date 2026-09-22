from django.contrib import admin
from .models import Restaurant

@admin.register(Restaurant)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'is_active', 'address', 'opening_time', 'closing_time')
    list_filter = ('is_active', )
    search_fields = ('name', 'phone')
