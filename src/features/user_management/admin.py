# User management admin configuration

from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """User profile admin interface"""
    
    list_display = ('user', 'location', 'is_public', 'created_at')
    list_filter = ('is_public', 'show_email', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'location')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Profile Information', {
            'fields': ('bio', 'avatar', 'date_of_birth', 'location', 'website')
        }),
        ('Privacy Settings', {
            'fields': ('is_public', 'show_email')
        }),
    )