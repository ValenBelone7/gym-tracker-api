"""
ViewSets para Workouts.

Endpoints:
- GET    /api/workouts/                    # Listar workouts
- POST   /api/workouts/                    # Crear workout
- GET    /api/workouts/{id}/               # Detalle
- PATCH  /api/workouts/{id}/               # Actualizar
- DELETE /api/workouts/{id}/               # Borrar
- POST   /api/workouts/{id}/exercises/     # Agregar ejercicio
- DELETE /api/workouts/{id}/exercises/{ex_id}/  # Quitar ejercicio
- POST   /api/workouts/{id}/exercises/{ex_id}/sets/  # Agregar set
- PATCH  /api/workouts/{id}/exercises/{ex_id}/sets/{set_id}/  # Actualizar set
- DELETE /api/workouts/{id}/exercises/{ex_id}/sets/{set_id}/  # Borrar set
- POST   /api/workouts/{id}/finish/        # Finalizar workout
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone

from core.permissions import IsOwner
from core.pagination import LargeResultsSetPagination
from .models import Workout, WorkoutExercise, Set
from .serializers import (
    WorkoutSerializer,
    WorkoutListSerializer,
    WorkoutExerciseCreateSerializer,
    SetCreateSerializer,
)


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar workouts del usuario.
    """
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = LargeResultsSetPagination
    
    def get_queryset(self):
        """Solo workouts del usuario actual"""
        return Workout.objects.filter(
            user=self.request.user
        ).select_related('routine').prefetch_related(
            'workout_exercises__exercise',
            'workout_exercises__sets'
        ).order_by('-date', '-created_at')
    
    def get_serializer_class(self):
        """Usar serializer ligero para lista"""
        if self.action == 'list':
            return WorkoutListSerializer
        return WorkoutSerializer
    
    def perform_create(self, serializer):
        """Asignar usuario actual y start_time"""
        serializer.save(
            user=self.request.user,
            start_time=timezone.now(),
            date=timezone.now().date()
        )
    
    @action(detail=True, methods=['post'], url_path='exercises')
    def add_exercise(self, request, pk=None):
        """
        POST /api/workouts/{id}/exercises/
        
        Agregar un ejercicio al workout.
        
        Body:
        {
            "exercise_id": 1,
            "order": 0,
            "notes": ""
        }
        """
        workout = self.get_object()
        
        serializer = WorkoutExerciseCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(workout=workout)
        
        # Retornar el workout actualizado
        workout_serializer = WorkoutSerializer(workout, context={'request': request})
        return Response(workout_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['delete'], url_path='exercises/(?P<exercise_id>[^/.]+)')
    def remove_exercise(self, request, pk=None, exercise_id=None):
        """
        DELETE /api/workouts/{id}/exercises/{exercise_id}/
        
        Quitar un ejercicio del workout.
        """
        workout = self.get_object()
        workout_exercise = get_object_or_404(
            WorkoutExercise,
            workout=workout,
            id=exercise_id
        )
        
        workout_exercise.delete()
        
        # Retornar el workout actualizado
        workout_serializer = WorkoutSerializer(workout, context={'request': request})
        return Response(workout_serializer.data)
    
    @action(
        detail=True,
        methods=['post'],
        url_path='exercises/(?P<exercise_id>[^/.]+)/sets'
    )
    def add_set(self, request, pk=None, exercise_id=None):
        """
        POST /api/workouts/{id}/exercises/{exercise_id}/sets/
        
        Agregar una serie a un ejercicio del workout.
        
        Body:
        {
            "set_number": 1,
            "weight": 100.5,
            "reps": 10,
            "completed": true,
            "rpe": 8
        }
        """
        workout = self.get_object()
        workout_exercise = get_object_or_404(
            WorkoutExercise,
            workout=workout,
            id=exercise_id
        )
        
        serializer = SetCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(workout_exercise=workout_exercise)
        
        # Retornar el workout actualizado
        workout_serializer = WorkoutSerializer(workout, context={'request': request})
        return Response(workout_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(
        detail=True,
        methods=['patch', 'delete'],
        url_path='exercises/(?P<exercise_id>[^/.]+)/sets/(?P<set_id>[^/.]+)'
    )
    def manage_set(self, request, pk=None, exercise_id=None, set_id=None):
        """
        PATCH  /api/workouts/{id}/exercises/{exercise_id}/sets/{set_id}/
        DELETE /api/workouts/{id}/exercises/{exercise_id}/sets/{set_id}/
        
        Actualizar o borrar una serie.
        """
        workout = self.get_object()
        workout_exercise = get_object_or_404(
            WorkoutExercise,
            workout=workout,
            id=exercise_id
        )
        set_obj = get_object_or_404(
            Set,
            workout_exercise=workout_exercise,
            id=set_id
        )
        
        if request.method == 'PATCH':
            serializer = SetCreateSerializer(
                set_obj,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            # Retornar el workout actualizado
            workout_serializer = WorkoutSerializer(workout, context={'request': request})
            return Response(workout_serializer.data)
        
        elif request.method == 'DELETE':
            set_obj.delete()
            
            # Retornar el workout actualizado
            workout_serializer = WorkoutSerializer(workout, context={'request': request})
            return Response(workout_serializer.data)
    
    @action(detail=True, methods=['post'], url_path='finish')
    def finish_workout(self, request, pk=None):
        """
        POST /api/workouts/{id}/finish/
        
        Finalizar el workout (setear end_time).
        """
        workout = self.get_object()
        
        if workout.end_time:
            return Response({
                'error': 'Este workout ya fue finalizado.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        workout.end_time = timezone.now()
        workout.save()
        
        serializer = WorkoutSerializer(workout, context={'request': request})
        return Response(serializer.data)