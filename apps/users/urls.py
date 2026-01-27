"""
URLs para autenticación y gestión de usuarios.
"""

from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    CurrentUserView,
    UpdateProfileView,
    ChangePasswordView,
    TestAuthView,
)

app_name = 'users'

urlpatterns = [
    # Autenticación
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/logout', LogoutView.as_view(), name='logout'),
    path('auth/me', CurrentUserView.as_view(), name='current-user'),
    
    # Gestión de perfil
    path('auth/profile', UpdateProfileView.as_view(), name='update-profile'),
    path('auth/change-password', ChangePasswordView.as_view(), name='change-password'),
    
    # Test
    path('auth/test/', TestAuthView.as_view(), name='test-auth'),
]