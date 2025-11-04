from typing import Optional
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import HttpRequest
from django.utils import timezone
from django.utils.html import format_html
from .models import PasswordResetToken

User = get_user_model()

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "full_name", "is_staff", "is_active", "last_login_display", "date_joined_display")
    list_filter = ("is_staff", "is_active", "is_superuser", "groups", "date_joined")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    filter_horizontal = ("groups", "user_permissions")
    readonly_fields = ("date_joined", "last_login")
    list_per_page = 25
    
    fieldsets = (
        (None, {
            "fields": ("email", "password"),
            "classes": ("wide",)
        }),
        ("Personal info", {
            "fields": ("first_name", "last_name"),
            "classes": ("wide",)
        }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
            "classes": ("collapse",)
        }),
        ("Important dates", {
            "fields": ("last_login", "date_joined"),
            "classes": ("collapse",)
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "first_name", "last_name",
                "password1", "password2",
                "is_active", "is_staff", "is_superuser"
            ),
        }),
    )

    def full_name(self, obj):
        return obj.get_full_name() or "No name provided"
    full_name.short_description = "Full Name"

    def last_login_display(self, obj):
        if obj.last_login:
            return self._format_date(obj.last_login)
        return "Never logged in"
    last_login_display.short_description = "Last Login"
    last_login_display.admin_order_field = 'last_login'

    def date_joined_display(self, obj):
        return self._format_date(obj.date_joined)
    date_joined_display.short_description = "Joined"
    date_joined_display.admin_order_field = 'date_joined'

    def _format_date(self, date):
        if not date:
            return "N/A"
        
        now = timezone.now()
        diff = now - date

        if diff.days == 0:
            if diff.seconds < 60:
                return "Just now"
            if diff.seconds < 3600:
                minutes = diff.seconds // 60
                return f"{minutes}m ago"
            hours = diff.seconds // 3600
            return f"{hours}h ago"
        if diff.days == 1:
            return "Yesterday"
        if diff.days < 7:
            return f"{diff.days}d ago"
        if diff.days < 30:
            weeks = diff.days // 7
            return f"{weeks}w ago"
        if diff.days < 365:
            months = diff.days // 30
            return f"{months}mo ago"
        years = diff.days // 365
        return f"{years}y ago"

@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'created_at_display', 'expires_at_display', 'is_expired_display')
    list_filter = ('created_at', 'expires_at')
    search_fields = ('user__email', 'code')
    readonly_fields = ('created_at', 'expires_at', 'code')
    ordering = ('-created_at',)
    list_per_page = 25
    
    fieldsets = (
        (None, {
            'fields': ('user', 'code')
        }),
        ('Timing Information', {
            'fields': ('created_at', 'expires_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'
    user_email.admin_order_field = 'user__email'
    
    def created_at_display(self, obj):
        return self._format_date(obj.created_at)
    created_at_display.short_description = 'Created'
    created_at_display.admin_order_field = 'created_at'
    
    def expires_at_display(self, obj):
        return self._format_date(obj.expires_at)
    expires_at_display.short_description = 'Expires'
    expires_at_display.admin_order_field = 'expires_at'
    
    def is_expired_display(self, obj):
        is_expired = obj.is_expired()
        color = 'red' if is_expired else 'green'
        text = 'Expired' if is_expired else 'Valid'
        return format_html('<span style="color: {};">{}</span>', color, text)
    is_expired_display.short_description = 'Status'
    
    def _format_date(self, date):
        if not date:
            return "N/A"
            
        now = timezone.now()
        diff = date - now if date > now else now - date
        
        if diff.days == 0:
            if diff.seconds < 60:
                return "Just now"
            if diff.seconds < 3600:
                minutes = diff.seconds // 60
                return f"{minutes} minutes"
            hours = diff.seconds // 3600
            return f"{hours} hours"
        if diff.days == 1:
            return "1 day"
        return f"{diff.days} days"
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False  # Prevent manual creation of reset tokens
        
    def has_change_permission(
        self, request: HttpRequest, obj: Optional[PasswordResetToken] = None
    ) -> bool:
        return False  # Prevent editing of reset tokens