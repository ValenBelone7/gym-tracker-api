"""
Modelos para Routines (plantillas de entrenamiento).

Una Routine es un template que contiene ejercicios organizados.
Ejemplo: "Push/Pull/Legs - Semana A"

Cuando el usuario va a entrenar, puede:
- Iniciar un Workout basado en una Routine (copia los ejercicios)
- Crear un Workout vacío (freestyle)
"""

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Routine(models.Model):
    """
    Plantilla de rutina de entrenamiento.
    
    Contiene una lista ordenada de ejercicios con metadata
    (sets objetivo, reps objetivo, notas).
    """
    
    name = models.CharField(
        max_length=100,
        help_text="Nombre de la rutina (ej: Push Day, Full Body A)"
    )
    description = models.TextField(
        blank=True,
        default="",
        help_text="Descripción o notas generales de la rutina"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='routines',
        help_text="Usuario propietario de esta rutina"
    )
    
    # Feature flag: marcar una rutina como "activa"
    # Útil para mostrar "Tu rutina actual" en el dashboard
    is_active = models.BooleanField(
        default=False,
        help_text="Rutina actualmente en uso"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'routines'
        ordering = ['-is_active', '-updated_at']
        verbose_name = 'rutina'
        verbose_name_plural = 'rutinas'
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['user', '-updated_at']),
        ]

    def __str__(self):
        active = " [ACTIVA]" if self.is_active else ""
        return f"{self.user.username} - {self.name}{active}"

    def save(self, *args, **kwargs):
        """
        Si marcamos esta rutina como activa, desactivar las demás del usuario.
        Solo puede haber una rutina activa por usuario.
        """
        if self.is_active:
            # Desactivar todas las otras rutinas del usuario
            Routine.objects.filter(
                user=self.user,
                is_active=True
            ).exclude(pk=self.pk).update(is_active=False)
        
        super().save(*args, **kwargs)
    
    @property
    def exercise_count(self):
        """Cantidad de ejercicios en esta rutina"""
        return self.routine_exercises.count()
    
    @property
    def estimated_duration(self):
        """
        Estimación de duración en minutos.
        
        Fórmula simple:
        - Cada ejercicio toma ~10 minutos (sets + descanso)
        - Mínimo 20 min, máximo 120 min
        """
        count = self.exercise_count
        duration = count * 10
        return max(20, min(120, duration))


class RoutineExercise(models.Model):
    """
    Relación N:M entre Routine y Exercise con metadata.
    
    Representa un ejercicio dentro de una rutina específica,
    con su orden, sets objetivo, reps objetivo, y notas.
    """
    
    routine = models.ForeignKey(
        Routine,
        on_delete=models.CASCADE,
        related_name='routine_exercises'
    )
    exercise = models.ForeignKey(
        'exercises.Exercise',
        on_delete=models.CASCADE,
        related_name='routine_exercises'
    )
    
    # Orden de ejecución dentro de la rutina
    order = models.PositiveIntegerField(
        default=0,
        help_text="Orden de ejecución (0, 1, 2, ...)"
    )
    
    # Objetivos del ejercicio en esta rutina
    target_sets = models.PositiveIntegerField(
        default=3,
        help_text="Cantidad de series objetivo"
    )
    target_reps = models.PositiveIntegerField(
        default=10,
        help_text="Cantidad de repeticiones objetivo por serie"
    )
    
    # Notas específicas para este ejercicio en esta rutina
    notes = models.TextField(
        blank=True,
        default="",
        help_text="Notas (ej: 'Descanso 2 min', 'Tempo 3-0-1')"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'routine_exercises'
        ordering = ['routine', 'order']
        verbose_name = 'ejercicio de rutina'
        verbose_name_plural = 'ejercicios de rutina'
        
        # Un ejercicio no puede estar duplicado en la misma rutina
        unique_together = [['routine', 'exercise']]
        
        indexes = [
            models.Index(fields=['routine', 'order']),
        ]

    def __str__(self):
        return f"{self.routine.name} - {self.exercise.name} (#{self.order + 1})"

    def clean(self):
        """
        Validaciones custom:
        - El ejercicio debe pertenecer al usuario (si es custom)
        """
        # Si el ejercicio es custom, debe pertenecer al mismo usuario que la rutina
        if not self.exercise.is_global:
            if self.exercise.created_by != self.routine.user:
                raise ValidationError({
                    'exercise': 'No podés usar ejercicios custom de otros usuarios.'
                })

    def save(self, *args, **kwargs):
        """Override save para ejecutar validaciones"""
        self.full_clean()
        super().save(*args, **kwargs)