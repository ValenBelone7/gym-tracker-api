"""
Modelos para Workouts (sesiones de entrenamiento reales).

Un Workout representa una sesión de entrenamiento que el usuario realizó o está realizando.
Puede estar basado en una Routine o ser freestyle.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal


class Workout(models.Model):
    """
    Sesión de entrenamiento.
    
    Puede estar basada en una Routine (copia sus ejercicios al inicio)
    o ser un workout freestyle (sin routine base).
    """
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='workouts',
        help_text="Usuario que realizó el workout"
    )
    routine = models.ForeignKey(
        'routines.Routine',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='workouts',
        help_text="Rutina base (opcional, puede ser None para freestyle)"
    )
    
    # Información temporal
    date = models.DateField(
        default=timezone.now,
        help_text="Fecha del workout"
    )
    start_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Hora de inicio del workout"
    )
    end_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Hora de finalización del workout"
    )
    
    # Notas generales del workout
    notes = models.TextField(
        blank=True,
        default="",
        help_text="Notas generales del entrenamiento"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'workouts'
        ordering = ['-date', '-created_at']
        verbose_name = 'entrenamiento'
        verbose_name_plural = 'entrenamientos'
        indexes = [
            models.Index(fields=['user', '-date']),
            models.Index(fields=['routine']),
            models.Index(fields=['-date']),
        ]

    def __str__(self):
        routine_name = self.routine.name if self.routine else "Freestyle"
        return f"{self.user.username} - {routine_name} ({self.date})"

    @property
    def duration(self):
        """Duración del workout en minutos"""
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            return int(delta.total_seconds() / 60)
        return None
    
    @property
    def total_volume(self):
        """
        Volumen total del workout (suma de peso x reps de todas las series).
        
        Retorna Decimal o 0 si no hay datos.
        """
        from django.db.models import Sum, F
        
        result = self.workout_exercises.aggregate(
            total=Sum(
                F('sets__weight') * F('sets__reps'),
                output_field=models.DecimalField()
            )
        )
        return result['total'] or Decimal('0')
    
    @property
    def total_sets(self):
        """Cantidad total de series realizadas"""
        return sum(
            we.sets.filter(completed=True).count() 
            for we in self.workout_exercises.all()
        )
    
    @property
    def exercise_count(self):
        """Cantidad de ejercicios realizados"""
        return self.workout_exercises.count()


class WorkoutExercise(models.Model):
    """
    Ejercicio realizado dentro de un Workout específico.
    
    Esta tabla permite flexibilidad:
    - Si el workout viene de una routine, se copian los ejercicios
    - Durante el workout, el usuario puede agregar/quitar ejercicios
    - No está atado al template original
    """
    
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        related_name='workout_exercises'
    )
    exercise = models.ForeignKey(
        'exercises.Exercise',
        on_delete=models.CASCADE,
        related_name='workout_exercises'
    )
    
    # Orden de ejecución en este workout
    order = models.PositiveIntegerField(
        default=0,
        help_text="Orden en que se realizó el ejercicio"
    )
    
    # Notas específicas para este ejercicio en este workout
    notes = models.TextField(
        blank=True,
        default="",
        help_text="Notas del día (ej: 'Sentí dolor en el hombro')"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'workout_exercises'
        ordering = ['workout', 'order']
        verbose_name = 'ejercicio de entrenamiento'
        verbose_name_plural = 'ejercicios de entrenamiento'
        
        # Un ejercicio no puede estar duplicado en el mismo workout
        unique_together = [['workout', 'exercise']]
        
        indexes = [
            models.Index(fields=['workout', 'order']),
            models.Index(fields=['exercise']),
        ]

    def __str__(self):
        return f"{self.workout} - {self.exercise.name}"
    
    @property
    def total_volume(self):
        """Volumen total de este ejercicio (suma de todas las series)"""
        from django.db.models import Sum, F
        
        result = self.sets.aggregate(
            total=Sum(
                F('weight') * F('reps'),
                output_field=models.DecimalField()
            )
        )
        return result['total'] or Decimal('0')


class Set(models.Model):
    """
    Serie individual dentro de un WorkoutExercise.
    
    Registra peso, reps, si se completó, y opcionalmente RPE.
    """
    
    workout_exercise = models.ForeignKey(
        WorkoutExercise,
        on_delete=models.CASCADE,
        related_name='sets'
    )
    
    # Número de serie (1, 2, 3, ...)
    set_number = models.PositiveIntegerField(
        help_text="Número de serie dentro del ejercicio"
    )
    
    # Datos de la serie
    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Peso utilizado en kg (null para ejercicios de peso corporal)"
    )
    reps = models.PositiveIntegerField(
        help_text="Repeticiones realizadas"
    )
    
    # Estado de la serie
    completed = models.BooleanField(
        default=True,
        help_text="Si la serie se completó exitosamente (False si falló)"
    )
    
    # RPE (Rate of Perceived Exertion)
    # Escala subjetiva de esfuerzo: 1-10
    rpe = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Esfuerzo percibido (1=muy fácil, 10=fallo muscular)"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sets'
        ordering = ['workout_exercise', 'set_number']
        verbose_name = 'serie'
        verbose_name_plural = 'series'
        
        # Un número de serie no puede estar duplicado en el mismo workout_exercise
        unique_together = [['workout_exercise', 'set_number']]
        
        indexes = [
            models.Index(fields=['workout_exercise', 'set_number']),
        ]

    def __str__(self):
        weight_str = f"{self.weight}kg" if self.weight else "BW"
        status = "✓" if self.completed else "✗"
        return f"{self.workout_exercise.exercise.name} - Set {self.set_number}: {weight_str} x {self.reps} {status}"

    @property
    def volume(self):
        """Volumen de esta serie (peso x reps)"""
        if self.weight:
            return float(self.weight) * self.reps
        return self.reps  # Para ejercicios de peso corporal
    
    def clean(self):
        """Validaciones custom"""
        from django.core.exceptions import ValidationError
        
        # Validar RPE si está presente
        if self.rpe is not None and (self.rpe < 1 or self.rpe > 10):
            raise ValidationError({
                'rpe': 'El RPE debe estar entre 1 y 10.'
            })
        
        # Validar que weight sea positivo si está presente
        if self.weight is not None and self.weight <= 0:
            raise ValidationError({
                'weight': 'El peso debe ser mayor a 0.'
            })
        
        # Validar que reps sea positivo
        if self.reps <= 0:
            raise ValidationError({
                'reps': 'Las repeticiones deben ser mayores a 0.'
            })

    def save(self, *args, **kwargs):
        """Override save para ejecutar validaciones"""
        self.full_clean()
        super().save(*args, **kwargs)