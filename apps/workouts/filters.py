"""
Filtros para la app `workouts`.
Permiten filtrar entrenamientos por duración, tipo o intensidad.
"""

from django_filters import rest_framework as filters


# class WorkoutFilter(filters.FilterSet):
#     class Meta:
#         model = Workout
#         fields = ['duration', 'intensity']
