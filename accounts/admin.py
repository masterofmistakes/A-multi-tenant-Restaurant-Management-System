from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomeUserAdmin(UserAdmin):
    ordering = ('fullname',)
    list_display = ('id','fullname', 'phone', 'role', 'is_staff', 'is_active', 'restaurant')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role', 'restaurant')
    search_fields = ('fullname',)

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Qosimsha magliwmatlar', {'fields': ('role', 'restaurant')}),
        ('Ruxsatlar', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Saneler:', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'role', 'restaurant'),
        }),
    )