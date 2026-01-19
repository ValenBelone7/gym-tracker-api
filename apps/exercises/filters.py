"""
Filters para búsqueda y filtrado de Exercises.

Permite:
- Buscar por nombre
- Filtrar por muscle_group
- Filtrar solo globales o solo custom
"""

from django_filters import rest_framework as filters
from .models import Exercise


class ExerciseFilter(filters.FilterSet):
    """
    FilterSet para Exercise.
    
    Ejemplos de uso:
    - /api/exercises/?search=bench
    - /api/exercises/?muscle_group=chest
    - /api/exercises/?is_global=true
    - /api/exercises/?search=press&muscle_group=shoulders
    """
    
    # Búsqueda por nombre (case-insensitive)
    search = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Buscar por nombre'
    )
    
    # Filtro por grupo muscular
    muscle_group = filters.ChoiceFilter(
        choices=Exercise.MUSCLE_GROUPS,
        label='Grupo muscular'
    )
    
    # Filtro global/custom
    is_global = filters.BooleanFilter(
        label='Solo ejercicios globales'
    )
    
    # Filtro para mostrar solo ejercicios del usuario actual
    # Este lo manejamos en el ViewSet, no aquí
    
    class Meta:
        model = Exercise
        fields = ['search', 'muscle_group', 'is_global']