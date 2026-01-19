"""
ViewSets para Routines.

Endpoints:
- GET    /api/routines/              # Listar rutinas del usuario
- POST   /api/routines/              # Crear rutina
- GET    /api/routines/{id}/         # Detalle de rutina
- PATCH  /api/routines/{id}/         # Actualizar rutina
- DELETE /api/routines/{id}/         # Borrar rutina
- POST   /api/routines/{id}/exercises/           # Agregar ejercicio
- PATCH  /api/routines/{id}/exercises/{ex_id}/   # Actualizar ejercicio
- DELETE /api/routines/{id}/exercises/{ex_id}/   # Quitar ejercicio
- POST   /api/routines/{id}/start-workout/       # Iniciar workout desde rutina
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from core.permissions import IsOwner
from core.pagination import StandardResultsSetPagination
from .models import Routine, RoutineExercise
from .serializers import (
    RoutineSerializer,
    RoutineListSerializer,
    RoutineExerciseSerializer,
    RoutineExerciseCreateSerializer,
    RoutineExerciseUpdateSerializer,
)


class RoutineViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar rutinas del usuario.
    """
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """Solo rutinas del usuario actual"""
        return Routine.objects.filter(
            user=self.request.user
        ).prefetch_related(
            'routine_exercises__exercise'
        ).order_by('-is_active', '-updated_at')
    
    def get_serializer_class(self):
        """Usar serializer ligero para lista"""
        if self.action == 'list':
            return RoutineListSerializer
        return RoutineSerializer
    
    def perform_create(self, serializer):
        """Asignar usuario actual al crear"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'], url_path='exercises')
    def add_exercise(self, request, pk=None):
        """
        POST /api/routines/{id}/exercises/
        
        Agregar un ejercicio a la rutina.
        
        Body:
        {
            "exercise_id": 1,
            "order": 0,
            "target_sets": 3,
            "target_reps": 10,
            "notes": ""
        }
        """
        routine = self.get_object()
        
        serializer = RoutineExerciseCreateSerializer(
            data=request.data,
            context={'request': request, 'routine': routine}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(routine=routine)
        
        # Retornar la rutina actualizada
        routine_serializer = RoutineSerializer(routine, context={'request': request})
        return Response(routine_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['patch', 'delete'], url_path='exercises/(?P<exercise_id>[^/.]+)')
    def manage_exercise(self, request, pk=None, exercise_id=None):
        """
        PATCH  /api/routines/{id}/exercises/{exercise_id}/
        DELETE /api/routines/{id}/exercises/{exercise_id}/
        
        Actualizar o eliminar un ejercicio de la rutina.
        """
        routine = self.get_object()
        routine_exercise = get_object_or_404(
            RoutineExercise,
            routine=routine,
            id=exercise_id
        )
        
        if request.method == 'PATCH':
            serializer = RoutineExerciseUpdateSerializer(
                routine_exercise,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            # Retornar la rutina actualizada
            routine_serializer = RoutineSerializer(routine, context={'request': request})
            return Response(routine_serializer.data)
        
        elif request.method == 'DELETE':
            routine_exercise.delete()
            
            # Retornar la rutina actualizada
            routine_serializer = RoutineSerializer(routine, context={'request': request})
            return Response(routine_serializer.data)
    
    @action(detail=True, methods=['post'], url_path='start-workout')
    def start_workout(self, request, pk=None):
        """
        POST /api/routines/{id}/start-workout/
        
        Crear un nuevo workout basado en esta rutina.
        Copia los ejercicios de la rutina al workout.
        
        Body (opcional):
        {
            "date": "2026-01-13",
            "notes": "Entrenamiento de hoy"
        }
        
        Returns: Workout creado con ejercicios copiados
        """
        routine = self.get_object()
        
        # Crear el workout
        from apps.workouts.models import Workout, WorkoutExercise
        from django.utils import timezone
        
        workout_data = {
            'user': request.user,
            'routine': routine,
            'date': request.data.get('date', timezone.now().date()),
            'notes': request.data.get('notes', ''),
            'start_time': timezone.now(),
        }
        
        workout = Workout.objects.create(**workout_data)
        
        # Copiar ejercicios de la rutina al workout
        for routine_exercise in routine.routine_exercises.all():
            WorkoutExercise.objects.create(
                workout=workout,
                exercise=routine_exercise.exercise,
                order=routine_exercise.order,
                notes=routine_exercise.notes,
            )
        
        # Serializar y retornar el workout creado
        from apps.workouts.serializers import WorkoutSerializer
        serializer = WorkoutSerializer(workout, context={'request': request})
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)