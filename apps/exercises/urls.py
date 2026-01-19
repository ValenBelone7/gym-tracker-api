"""
URLs para Exercises API.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExerciseViewSet

app_name = 'exercises'

# Router para ViewSets
router = DefaultRouter()
router.register(r'exercises', ExerciseViewSet, basename='exercise')

urlpatterns = [
    path('', include(router.urls)),
]