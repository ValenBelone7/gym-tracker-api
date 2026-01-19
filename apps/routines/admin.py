"""
Django admin para Routines.
"""

from django.contrib import admin
from .models import Routine, RoutineExercise


class RoutineExerciseInline(admin.TabularInline):
    """
    Inline para editar ejercicios dentro de una rutina.
    Permite agregar/editar/eliminar ejercicios sin salir de la vista de Routine.
    """
    model = RoutineExercise
    extra = 1
    fields = ['exercise', 'order', 'target_sets', 'target_reps', 'notes']
    ordering = ['order']
    autocomplete_fields = ['exercise']


@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    """
    Admin para gestionar rutinas.
    """
    list_display = [
        'name',
        'user',
        'is_active',
        'exercise_count',
        'estimated_duration',
        'created_at'
    ]
    list_filter = ['is_active', 'created_at', 'user']
    search_fields = ['name', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at', 'exercise_count', 'estimated_duration']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('name', 'description', 'user')
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('exercise_count', 'estimated_duration', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [RoutineExerciseInline]
    
    def get_queryset(self, request):
        """Optimizar query con select_related y prefetch_related"""
        qs = super().get_queryset(request)
        return qs.select_related('user').prefetch_related('routine_exercises__exercise')


@admin.register(RoutineExercise)
class RoutineExerciseAdmin(admin.ModelAdmin):
    """
    Admin para gestionar ejercicios de rutinas (por si se necesita acceso directo).
    """
    list_display = [
        'routine',
        'exercise',
        'order',
        'target_sets',
        'target_reps'
    ]
    list_filter = ['routine__user', 'exercise__muscle_group']
    search_fields = ['routine__name', 'exercise__name']
    ordering = ['routine', 'order']
    
    autocomplete_fields = ['routine', 'exercise']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('routine', 'exercise')