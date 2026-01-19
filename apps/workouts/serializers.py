"""
Serializers para Workouts.

Maneja la serialización nested de Workout → WorkoutExercise → Set.
"""

from rest_framework import serializers
from apps.exercises.serializers import ExerciseListSerializer
from apps.exercises.models import Exercise
from .models import Workout, WorkoutExercise, Set


class SetSerializer(serializers.ModelSerializer):
    """
    Serializer para Set (serie individual).
    """
    volume = serializers.ReadOnlyField()
    
    class Meta:
        model = Set
        fields = [
            'id',
            'set_number',
            'weight',
            'reps',
            'completed',
            'rpe',
            'volume',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate(self, attrs):
        """Validaciones adicionales"""
        # Validar RPE si está presente
        rpe = attrs.get('rpe')
        if rpe is not None and (rpe < 1 or rpe > 10):
            raise serializers.ValidationError({
                'rpe': 'El RPE debe estar entre 1 y 10.'
            })
        
        # Validar weight si está presente
        weight = attrs.get('weight')
        if weight is not None and weight <= 0:
            raise serializers.ValidationError({
                'weight': 'El peso debe ser mayor a 0.'
            })
        
        # Validar reps
        reps = attrs.get('reps')
        if reps and reps <= 0:
            raise serializers.ValidationError({
                'reps': 'Las repeticiones deben ser mayores a 0.'
            })
        
        return attrs


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    """
    Serializer para WorkoutExercise (ejercicio dentro de un workout).
    Incluye ejercicio y sets nested.
    """
    exercise = ExerciseListSerializer(read_only=True)
    exercise_id = serializers.PrimaryKeyRelatedField(
        queryset=Exercise.objects.all(),
        source='exercise',
        write_only=True
    )
    sets = SetSerializer(many=True, read_only=True)
    total_volume = serializers.ReadOnlyField()
    
    class Meta:
        model = WorkoutExercise
        fields = [
            'id',
            'exercise',
            'exercise_id',
            'order',
            'notes',
            'sets',
            'total_volume',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            from django.db.models import Q
            
            self.fields['exercise_id'].queryset = Exercise.objects.filter(
                Q(is_global=True) | Q(created_by=request.user)
            )


class WorkoutSerializer(serializers.ModelSerializer):
    """
    Serializer completo para Workout.
    Incluye ejercicios y sets nested.
    """
    workout_exercises = WorkoutExerciseSerializer(many=True, read_only=True)
    routine_name = serializers.CharField(source='routine.name', read_only=True, allow_null=True)
    
    # Propiedades calculadas
    duration = serializers.ReadOnlyField()
    total_volume = serializers.ReadOnlyField()
    total_sets = serializers.ReadOnlyField()
    exercise_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Workout
        fields = [
            'id',
            'routine',
            'routine_name',
            'date',
            'start_time',
            'end_time',
            'duration',
            'notes',
            'workout_exercises',
            'total_volume',
            'total_sets',
            'exercise_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Asignar automáticamente el usuario actual"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class WorkoutListSerializer(serializers.ModelSerializer):
    """
    Serializer ligero para lista de workouts.
    No incluye ejercicios nested (performance).
    """
    routine_name = serializers.CharField(source='routine.name', read_only=True, allow_null=True)
    duration = serializers.ReadOnlyField()
    total_volume = serializers.ReadOnlyField()
    exercise_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Workout
        fields = [
            'id',
            'routine_name',
            'date',
            'duration',
            'total_volume',
            'exercise_count',
            'created_at',
        ]


class WorkoutExerciseCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para agregar ejercicios a un workout.
    """
    exercise_id = serializers.PrimaryKeyRelatedField(
        queryset=Exercise.objects.all(),
        source='exercise'
    )
    
    class Meta:
        model = WorkoutExercise
        fields = ['exercise_id', 'order', 'notes']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            from django.db.models import Q
            
            self.fields['exercise_id'].queryset = Exercise.objects.filter(
                Q(is_global=True) | Q(created_by=request.user)
            )


class SetCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear/actualizar sets.
    """
    
    class Meta:
        model = Set
        fields = ['set_number', 'weight', 'reps', 'completed', 'rpe']
    
    def validate(self, attrs):
        """Validaciones"""
        rpe = attrs.get('rpe')
        if rpe is not None and (rpe < 1 or rpe > 10):
            raise serializers.ValidationError({
                'rpe': 'El RPE debe estar entre 1 y 10.'
            })
        
        weight = attrs.get('weight')
        if weight is not None and weight <= 0:
            raise serializers.ValidationError({
                'weight': 'El peso debe ser mayor a 0.'
            })
        
        reps = attrs.get('reps')
        if reps and reps <= 0:
            raise serializers.ValidationError({
                'reps': 'Las repeticiones deben ser mayores a 0.'
            })
        
        return attrs