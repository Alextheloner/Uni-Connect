from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'school', 'department', 'reputation']
    list_filter = ['role', 'school', 'department', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    autocomplete_fields = ['school', 'department']
    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {'fields': ('role', 'school', 'department', 'matric_number', 'bio', 'avatar', 'reputation')}),
    )
