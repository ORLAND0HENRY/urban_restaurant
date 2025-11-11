from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Reservation model.

    list_display is updated to only include fields present in the Reservation model.
    """
    list_display = (
        'user',
        'date',
        'time',
        'party_size',
        'status',
        'created_at'
    )

    list_filter = ('status', 'date', 'time', 'party_size')

    search_fields = (
        'user__username',
        'user__email',
        'date',
        'status'
    )

    date_hierarchy = 'date'
    ordering = ('-date', 'time')