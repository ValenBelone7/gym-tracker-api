"""
Django admin para Workouts.
"""

from django.contrib import admin
from .models import Workout, WorkoutExercise, Set


class SetInline(admin.TabularInline):
    """Inline para editar series dentro de un WorkoutExercise"""
    model = Set
    extra = 1
    fields = ['set_number', 'weight', 'reps', 'completed', 'rpe']
    ordering = ['set_number']


class WorkoutExerciseInline(admin.TabularInline):
    """Inline para editar ejercicios dentro de un Workout"""
    model = WorkoutExercise
    extra = 0
    fields = ['exercise', 'order', 'notes']
    ordering = ['order']
    autocomplete_fields = ['exercise']
    show_change_link = True  # Link para editar las series


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """Admin para gestionar workouts"""
    list_display = [
        'user',
        'routine',
        'date',
        'duration',
        'exercise_count',
        'total_sets',
        'total_volume'
    ]
    list_filter = ['date', 'user', 'routine']
    search_fields = ['user__username', 'routine__name', 'notes']
    date_hierarchy = 'date'
    readonly_fields = [
        'created_at',
        'updated_at',
        'duration',
        'exercise_count',
        'total_sets',
        'total_volume'
    ]
    
    fieldsets = (
        ('Información básica', {
            'fields': ('user', 'routine', 'date')
        }),
        ('Tiempo', {
            'fields': ('start_time', 'end_time', 'duration')
        }),
        ('Notas', {
            'fields': ('notes',)
        }),
        ('Estadísticas', {
            'fields': ('exercise_count', 'total_sets', 'total_volume'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [WorkoutExerciseInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'routine').prefetch_related(
            'workout_exercises__exercise',
            'workout_exercises__sets'
        )


@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    """Admin para gestionar ejercicios de workouts"""
    list_display = [
        'workout',
        'exercise',
        'order',
        'sets_count',
        'total_volume'
    ]
    list_filter = ['workout__user', 'exercise__muscle_group', 'workout__date']
    search_fields = ['workout__user__username', 'exercise__name']
    ordering = ['workout', 'order']
    
    autocomplete_fields = ['workout', 'exercise']
    readonly_fields = ['total_volume']
    
    inlines = [SetInline]
    
    def sets_count(self, obj):
        return obj.sets.count()
    sets_count.short_description = 'Sets'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('workout', 'exercise').prefetch_related('sets')


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    """Admin para gestionar series individuales"""
    list_display = [
        'workout_exercise',
        'set_number',
        'weight',
        'reps',
        'completed',
        'rpe',
        'volume'
    ]
    list_filter = [
        'completed',
        'workout_exercise__workout__date',
        'workout_exercise__exercise__muscle_group'
    ]
    search_fields = [
        'workout_exercise__workout__user__username',
        'workout_exercise__exercise__name'
    ]
    ordering = ['workout_exercise', 'set_number']
    
    autocomplete_fields = ['workout_exercise']
    readonly_fields = ['volume', 'created_at']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'workout_exercise__workout__user',
            'workout_exercise__exercise'
        )