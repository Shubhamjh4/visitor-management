from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Employee, Visitor, Visit


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "phone", "email", "active")
    list_filter = ("active", "department")
    search_fields = ("name", "phone", "email", "department")
    list_editable = ("active",)
    ordering = ("name",)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'phone', 'email')
        }),
        ('Work Details', {
            'fields': ('department', 'active')
        }),
    )


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "address", "govt_id_type", "created_at")
    search_fields = ("full_name", "phone", "address")
    list_filter = ("govt_id_type", "created_at")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'phone', 'address')
        }),
        ('Government ID', {
            'fields': ('govt_id_type',)
        }),
        ('Documents', {
            'fields': ('photo', 'govt_id_image')
        }),
        ('System Info', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ("visitor", "employee", "status", "purpose", "started_at", "ended_at", "duration")
    list_filter = ("status", "employee", "started_at", "ended_at")
    search_fields = ("visitor__full_name", "employee__name", "purpose")
    readonly_fields = ("started_at", "ended_at", "sms_sent_at")
    ordering = ("-started_at",)
    
    def duration(self, obj):
        if obj.started_at and obj.ended_at:
            duration = obj.ended_at - obj.started_at
            hours, remainder = divmod(duration.total_seconds(), 3600)
            minutes, _ = divmod(remainder, 60)
            return f"{int(hours)}h {int(minutes)}m"
        elif obj.started_at:
            return "Ongoing"
        return "-"
    duration.short_description = "Duration"
    
    fieldsets = (
        ('Visit Details', {
            'fields': ('visitor', 'employee', 'purpose', 'status')
        }),
        ('Timing', {
            'fields': ('started_at', 'ended_at', 'sms_sent_at')
        }),
    )


# Enhanced User Admin
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)

# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register your models here.
