"""
Permissions personalizadas para el proyecto.

Estas permissions se usan en los ViewSets para controlar
qué usuarios pueden hacer qué acciones.
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission que permite:
    - Lectura a cualquier usuario autenticado
    - Escritura solo al owner del objeto
    
    Uso: Para objetos que tienen un campo 'user' o 'created_by'
    """
    
    def has_object_permission(self, request, view, obj):
        # Lectura permitida para cualquier usuario autenticado
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Escritura solo para el owner
        # Intentamos con 'user' primero, si no existe probamos 'created_by'
        owner = getattr(obj, 'user', None) or getattr(obj, 'created_by', None)
        return owner == request.user


class IsOwner(permissions.BasePermission):
    """
    Permission que solo permite acceso al owner del objeto.
    Más restrictivo que IsOwnerOrReadOnly.
    
    Uso: Para datos sensibles como workouts, rutinas personales.
    """
    
    def has_object_permission(self, request, view, obj):
        owner = getattr(obj, 'user', None) or getattr(obj, 'created_by', None)
        return owner == request.user


class IsOwnerOrGlobal(permissions.BasePermission):
    """
    Permission especial para Exercises:
    - Ejercicios globales: solo lectura
    - Ejercicios custom: lectura/escritura para el owner
    
    Previene que usuarios modifiquen ejercicios globales.
    """
    
    def has_object_permission(self, request, view, obj):
        # Si es global, solo lectura
        if getattr(obj, 'is_global', False):
            return request.method in permissions.SAFE_METHODS
        
        # Si no es global, verificar ownership
        owner = getattr(obj, 'created_by', None)
        return owner == request.user