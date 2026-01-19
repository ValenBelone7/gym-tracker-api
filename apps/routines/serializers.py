"""
Serializers para Routines.

Maneja la serialización nested de Routine → RoutineExercise → Exercise.
"""

from rest_framework import serializers
from apps.exercises.serializers import ExerciseListSerializer
from apps.exercises.models import Exercise
from .models import Routine, RoutineExercise


class RoutineExerciseSerializer(serializers.ModelSerializer):
    """
    Serializer para RoutineExercise (ejercicio dentro de una rutina).
    Incluye datos del Exercise anidado.
    """
    exercise = ExerciseListSerializer(read_only=True)
    exercise_id = serializers.PrimaryKeyRelatedField(
        queryset=Exercise.objects.all(),
        source='exercise',
        write_only=True,
        help_text="ID del ejercicio"
    )
    
    class Meta:
        model = RoutineExercise
        fields = [
            'id',
            'exercise',
            'exercise_id',
            'order',
            'target_sets',
            'target_reps',
            'notes',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configurar queryset de exercise_id basado en el usuario
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            from django.db.models import Q
            
            # Usuario puede usar ejercicios globales o sus propios custom
            self.fields['exercise_id'].queryset = Exercise.objects.filter(
                Q(is_global=True) | Q(created_by=request.user)
            )


class RoutineSerializer(serializers.ModelSerializer):
    """
    Serializer completo para Routine.
    Incluye lista de ejercicios nested.
    """
    routine_exercises = RoutineExerciseSerializer(many=True, read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    # Propiedades calculadas
    exercise_count = serializers.ReadOnlyField()
    estimated_duration = serializers.ReadOnlyField()
    
    class Meta:
        model = Routine
        fields = [
            'id',
            'name',
            'description',
            'user',
            'user_username',
            'is_active',
            'routine_exercises',
            'exercise_count',
            'estimated_duration',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Asignar automáticamente el usuario actual"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class RoutineListSerializer(serializers.ModelSerializer):
    """
    Serializer ligero para lista de rutinas.
    No incluye ejercicios nested (performance).
    """
    exercise_count = serializers.ReadOnlyField()
    estimated_duration = serializers.ReadOnlyField()
    
    class Meta:
        model = Routine
        fields = [
            'id',
            'name',
            'description',
            'is_active',
            'exercise_count',
            'estimated_duration',
            'created_at',
            'updated_at',
        ]


class RoutineExerciseCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para agregar ejercicios a una rutina.
    Usado en endpoint: POST /api/routines/{id}/exercises/
    """
    
    class Meta:
        model = RoutineExercise
        fields = [
            'exercise_id',
            'order',
            'target_sets',
            'target_reps',
            'notes',
        ]
    
    exercise_id = serializers.PrimaryKeyRelatedField(
        queryset=Exercise.objects.all(),
        source='exercise',
        help_text="ID del ejercicio a agregar"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            from django.db.models import Q
            
            self.fields['exercise_id'].queryset = Exercise.objects.filter(
                Q(is_global=True) | Q(created_by=request.user)
            )
    
    def validate(self, attrs):
        """
        Validar que el ejercicio no esté ya en la rutina.
        """
        routine = self.context.get('routine')
        exercise = attrs.get('exercise')
        
        if routine and exercise:
            if RoutineExercise.objects.filter(
                routine=routine,
                exercise=exercise
            ).exists():
                raise serializers.ValidationError({
                    'exercise_id': 'Este ejercicio ya está en la rutina.'
                })
        
        return attrs


class RoutineExerciseUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para actualizar ejercicios de una rutina.
    Solo permite modificar order, target_sets, target_reps, notes.
    No permite cambiar el ejercicio (para eso hay que borrarlo y agregar otro).
    """
    
    class Meta:
        model = RoutineExercise
        fields = ['order', 'target_sets', 'target_reps', 'notes']