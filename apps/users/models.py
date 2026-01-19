"""
User model extendido.

Decisión: Heredar de AbstractUser (no AbstractBaseUser) porque:
- Ya tiene username, email, password, is_staff, etc.
- Es menos trabajo y más compatible con Django admin
- Podemos agregar campos custom sin reinventar la rueda
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Usuario extendido con campos adicionales para el perfil.
    
    Campos heredados de AbstractUser:
    - username
    - email
    - first_name
    - last_name
    - password
    - is_staff
    - is_active
    - is_superuser
    - date_joined
    - last_login
    """
    
    # Campos adicionales para futuro
    bio = models.TextField(
        blank=True, 
        default="",
        help_text="Biografía o descripción del usuario"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        """Devuelve nombre completo o username si no hay nombre"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username