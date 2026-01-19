"""
URLs para Routines API.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoutineViewSet

app_name = 'routines'

router = DefaultRouter()
router.register(r'routines', RoutineViewSet, basename='routine')

urlpatterns = [
    path('', include(router.urls)),
]