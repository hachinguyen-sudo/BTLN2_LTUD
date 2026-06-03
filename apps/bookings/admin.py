from django.contrib import admin
from .models import Booking, Payment, Promotion


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display  = ['code', 'discount_percent', 'start_date', 'end_date', 'is_active']
    list_editable = ['is_active']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display    = ['id', 'user', 'service', 'booking_date', 'time_slot', 'status']
    list_filter     = ['status', 'booking_date']
    search_fields   = ['user__username', 'user__customerprofile__phone']
    readonly_fields = ['user', 'service', 'promotion', 'address', 'district',
                       'booking_date', 'time_slot', 'note', 'total_amount', 'created_at']

    def has_add_permission(self, request):
        return False


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display    = ['id', 'booking', 'amount', 'method', 'status', 'paid_at']
    readonly_fields = ['booking', 'amount', 'method', 'status', 'paid_at']

    def has_add_permission(self, request):
        return False