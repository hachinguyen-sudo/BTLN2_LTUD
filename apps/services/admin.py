from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display  = ['id', 'name', 'price', 'duration_hours', 'is_active']
    list_filter   = ['is_active']
    list_editable = ['is_active']
    search_fields = ['name']