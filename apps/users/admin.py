"""
Django admin para User model.
Extiende UserAdmin para incluir campos custom.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin personalizado para User.
    Hereda de UserAdmin para mantener toda la funcionalidad.
    """
    
    # Campos a mostrar en la lista
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'created_at']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    # Agregar campos custom a los fieldsets
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': ('bio', 'created_at', 'updated_at')
        }),
    )
    
    # Campos readonly
    readonly_fields = ['created_at', 'updated_at', 'date_joined', 'last_login']
    
    # Campos en el formulario de creación
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Información adicional', {
            'fields': ('email', 'first_name', 'last_name')
        }),
    )