"""
Exercise model.

Sistema híbrido:
- Ejercicios globales (seed data, is_global=True)
- Ejercicios custom por usuario (created_by != None)
"""

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Exercise(models.Model):
    """
    Catálogo de ejercicios.
    
    Puede ser:
    1. Global: Ejercicios pre-cargados visibles para todos
    2. Custom: Ejercicios creados por usuarios específicos
    """
    
    MUSCLE_GROUPS = [
        ('chest', 'Pecho'),
        ('back', 'Espalda'),
        ('legs', 'Piernas'),
        ('shoulders', 'Hombros'),
        ('arms', 'Brazos'),
        ('core', 'Core'),
        ('cardio', 'Cardio'),
        ('other', 'Otro'),
    ]

    name = models.CharField(
        max_length=100,
        help_text="Nombre del ejercicio (ej: Bench Press)"
    )
    description = models.TextField(
        blank=True, 
        default="",
        help_text="Descripción o instrucciones del ejercicio"
    )
    muscle_group = models.CharField(
        max_length=20, 
        choices=MUSCLE_GROUPS,
        help_text="Grupo muscular principal"
    )
    
    # Sistema híbrido global/custom
    is_global = models.BooleanField(
        default=False,
        help_text="Si es True, el ejercicio es visible para todos"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='custom_exercises',
        help_text="Usuario que creó este ejercicio (None si es global)"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'exercises'
        ordering = ['muscle_group', 'name']
        verbose_name = 'ejercicio'
        verbose_name_plural = 'ejercicios'
        
        # Un usuario no puede tener dos ejercicios con el mismo nombre
        # Los ejercicios globales (created_by=None) no tienen esta restricción
        unique_together = [['name', 'created_by']]
        
        indexes = [
            models.Index(fields=['is_global', 'muscle_group']),
            models.Index(fields=['created_by']),
        ]

    def __str__(self):
        prefix = "[Global]" if self.is_global else f"[{self.created_by.username}]"
        return f"{prefix} {self.name}"

    def clean(self):
        """
        Validación custom: Si es global, no debe tener creador.
        """
        if self.is_global and self.created_by is not None:
            raise ValidationError({
                'created_by': 'Los ejercicios globales no pueden tener un creador específico.'
            })
        
        if not self.is_global and self.created_by is None:
            raise ValidationError({
                'created_by': 'Los ejercicios no globales deben tener un creador.'
            })

    def save(self, *args, **kwargs):
        """Override save para ejecutar validaciones"""
        self.full_clean()
        super().save(*args, **kwargs)