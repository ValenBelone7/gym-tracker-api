"""
Paginación personalizada para APIs.

Formato de respuesta consistente con metadata útil.
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    """
    Paginación estándar del proyecto.
    
    Retorna formato:
    {
        "count": 100,
        "next": "http://api.example.org/accounts/?page=3",
        "previous": "http://api.example.org/accounts/?page=1",
        "results": [...]
    }
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class LargeResultsSetPagination(PageNumberPagination):
    """
    Paginación para listas grandes (ej: workouts history).
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200


class SmallResultsSetPagination(PageNumberPagination):
    """
    Paginación para listas pequeñas (ej: rutinas activas).
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50