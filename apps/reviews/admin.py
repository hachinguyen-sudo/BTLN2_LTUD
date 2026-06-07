from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display    = ['id', 'booking', 'rating', 'is_visible', 'created_at']
    list_editable   = ['is_visible']
    readonly_fields = ['booking', 'rating', 'comment', 'created_at']

    def has_add_permission(self, request):
        return False