from django.contrib import admin
from .models import Category

@admin.register(Category)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'restaurant')
    list_filter = ('restaurant', )
    search_fields = ('name', 'parent')
    