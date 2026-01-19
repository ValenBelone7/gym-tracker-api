"""
Serializers para Exercise model.
"""

from rest_framework import serializers
from .models import Exercise


class ExerciseSerializer(serializers.ModelSerializer):
    """
    Serializer completo de Exercise.
    
    Maneja tanto ejercicios globales como custom.
    """
    created_by_username = serializers.CharField(
        source='created_by.username',
        read_only=True,
        allow_null=True
    )
    muscle_group_display = serializers.CharField(
        source='get_muscle_group_display',
        read_only=True
    )
    
    class Meta:
        model = Exercise
        fields = [
            'id',
            'name',
            'description',
            'muscle_group',
            'muscle_group_display',
            'is_global',
            'created_by',
            'created_by_username',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'is_global', 'created_by', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """
        Al crear, asignar automáticamente el usuario actual como creador.
        Los ejercicios custom siempre tienen is_global=False.
        """
        validated_data['created_by'] = self.context['request'].user
        validated_data['is_global'] = False
        return super().create(validated_data)
    
    def validate_name(self, value):
        """
        Validar que el nombre no esté duplicado para este usuario.
        Los ejercicios globales con el mismo nombre están OK (diferente creador).
        """
        user = self.context['request'].user
        
        # Si estamos editando, excluir el objeto actual
        instance = self.instance
        queryset = Exercise.objects.filter(
            name__iexact=value,
            created_by=user
        )
        
        if instance:
            queryset = queryset.exclude(pk=instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError(
                'Ya tenés un ejercicio con este nombre.'
            )
        
        return value


class ExerciseListSerializer(serializers.ModelSerializer):
    """
    Serializer ligero para listas de ejercicios.
    Menos campos para mejor performance.
    """
    muscle_group_display = serializers.CharField(
        source='get_muscle_group_display',
        read_only=True
    )
    is_custom = serializers.SerializerMethodField()
    
    class Meta:
        model = Exercise
        fields = [
            'id',
            'name',
            'muscle_group',
            'muscle_group_display',
            'is_global',
            'is_custom',
        ]
    
    def get_is_custom(self, obj):
        """Verificar si es un ejercicio custom del usuario actual"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.created_by == request.user
        return False