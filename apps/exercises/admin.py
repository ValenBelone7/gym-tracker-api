"""
Django admin para Exercise model.
"""

from django.contrib import admin
from .models import Exercise


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    """
    Admin para gestionar ejercicios globales y custom.
    """
    
    list_display = [
        'name', 
        'muscle_group', 
        'is_global', 
        'created_by', 
        'created_at'
    ]
    
    list_filter = [
        'is_global', 
        'muscle_group', 
        'created_at'
    ]
    
    search_fields = [
        'name', 
        'description', 
        'created_by__username'
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('name', 'description', 'muscle_group')
        }),
        ('Configuración', {
            'fields': ('is_global', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """
        Optimizar query con select_related para evitar N+1.
        """
        qs = super().get_queryset(request)
        return qs.select_related('created_by')