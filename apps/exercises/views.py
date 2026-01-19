"""
ViewSet para Exercise model.

Endpoints:
- GET    /api/exercises/          # Listar (globales + custom del user)
- POST   /api/exercises/          # Crear custom
- GET    /api/exercises/:id/      # Detalle
- PATCH  /api/exercises/:id/      # Actualizar custom
- DELETE /api/exercises/:id/      # Borrar custom
"""

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from core.permissions import IsOwnerOrGlobal
from core.pagination import StandardResultsSetPagination
from .models import Exercise
from .serializers import ExerciseSerializer, ExerciseListSerializer
from .filters import ExerciseFilter


class ExerciseViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar ejercicios.
    
    Lógica:
    - Los usuarios ven ejercicios globales + sus propios custom
    - Solo pueden editar/borrar sus propios custom
    - No pueden editar/borrar globales
    """
    permission_classes = [IsAuthenticated, IsOwnerOrGlobal]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ExerciseFilter
    ordering_fields = ['name', 'muscle_group', 'created_at']
    ordering = ['muscle_group', 'name']
    
    def get_queryset(self):
        """
        Retornar ejercicios globales + custom del usuario actual.
        """
        user = self.request.user
        return Exercise.objects.filter(
            models.Q(is_global=True) | models.Q(created_by=user)
        ).select_related('created_by')
    
    def get_serializer_class(self):
        """
        Usar serializer ligero para listas, completo para detalle.
        """
        if self.action == 'list':
            return ExerciseListSerializer
        return ExerciseSerializer
    
    def perform_create(self, serializer):
        """
        Al crear, asignar usuario actual.
        El serializer ya maneja is_global=False.
        """
        serializer.save()
    
    def destroy(self, request, *args, **kwargs):
        """
        Prevenir borrado de ejercicios globales.
        """
        instance = self.get_object()
        
        if instance.is_global:
            return Response({
                'error': 'No se pueden borrar ejercicios globales.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        if instance.created_by != request.user:
            return Response({
                'error': 'No podés borrar ejercicios de otros usuarios.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        """
        Prevenir edición de ejercicios globales.
        """
        instance = self.get_object()
        
        if instance.is_global:
            return Response({
                'error': 'No se pueden editar ejercicios globales.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        if instance.created_by != request.user:
            return Response({
                'error': 'No podés editar ejercicios de otros usuarios.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        return super().update(request, *args, **kwargs)


# Importar Q para el queryset
from django.db import models