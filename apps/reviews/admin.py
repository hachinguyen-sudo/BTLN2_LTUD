from django.contrib import admin
from .models import Review, Contact


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display    = ['id', 'booking', 'rating', 'is_visible', 'created_at']
    list_editable   = ['is_visible']
    readonly_fields = ['booking', 'rating', 'comment', 'created_at']

    def has_add_permission(self, request):
        return False


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display    = ['name', 'phone', 'email', 'is_read', 'created_at']
    list_editable   = ['is_read']
    readonly_fields = ['name', 'phone', 'email', 'message', 'created_at']

    def has_add_permission(self, request):
        return False
    
