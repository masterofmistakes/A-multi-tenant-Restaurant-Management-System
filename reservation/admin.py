from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'restaurant',
        'table',
        'client',
        'start_time',
        'status',
    )

    list_filter = ('status', 'restaurant')

    search_fields = ('table__number', 'client__username')

    readonly_fields = ('end_time', 'created_at')