"""
Excepciones personalizadas para el proyecto.

Estas permiten tener mensajes de error consistentes
y códigos HTTP apropiados.
"""

from rest_framework.exceptions import APIException
from rest_framework import status


class BusinessLogicError(APIException):
    """
    Error de lógica de negocio genérico.
    
    Ejemplo: Intentar crear un workout sin exercises.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Error en la lógica de negocio.'
    default_code = 'business_logic_error'


class ResourceConflict(APIException):
    """
    Conflicto con un recurso existente.
    
    Ejemplo: Intentar crear un ejercicio con nombre duplicado.
    """
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'El recurso ya existe.'
    default_code = 'resource_conflict'


class InsufficientPermissions(APIException):
    """
    El usuario no tiene permisos suficientes.
    
    Diferente de 403 Forbidden, este es para lógica de negocio.
    Ejemplo: Intentar editar un workout de otro usuario.
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'No tienes permisos para realizar esta acción.'
    default_code = 'insufficient_permissions'