"""
Management command para cargar ejercicios globales iniciales.

Uso:
    python manage.py seed_exercises
    python manage.py seed_exercises --clear  # Borra ejercicios globales existentes
"""

from django.core.management.base import BaseCommand
from apps.exercises.models import Exercise


class Command(BaseCommand):
    help = 'Carga ejercicios globales iniciales en la base de datos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Borra ejercicios globales existentes antes de cargar',
        )

    def handle(self, *args, **options):
        if options['clear']:
            count = Exercise.objects.filter(is_global=True).count()
            Exercise.objects.filter(is_global=True).delete()
            self.stdout.write(
                self.style.WARNING(f'✓ Borrados {count} ejercicios globales existentes')
            )

        exercises_data = [
            # PECHO
            {
                'name': 'Bench Press (Barra)',
                'description': 'Press de banca con barra. Ejercicio compuesto fundamental para pecho.',
                'muscle_group': 'chest',
            },
            {
                'name': 'Incline Bench Press',
                'description': 'Press en banco inclinado (30-45°) para énfasis en pecho superior.',
                'muscle_group': 'chest',
            },
            {
                'name': 'Dumbbell Fly',
                'description': 'Aperturas con mancuernas para aislamiento de pectorales.',
                'muscle_group': 'chest',
            },
            {
                'name': 'Push-ups',
                'description': 'Flexiones de brazos. Ejercicio con peso corporal.',
                'muscle_group': 'chest',
            },
            
            # ESPALDA
            {
                'name': 'Pull-ups',
                'description': 'Dominadas con agarre pronado. Ejercicio compuesto para espalda.',
                'muscle_group': 'back',
            },
            {
                'name': 'Barbell Row',
                'description': 'Remo con barra. Ejercicio compuesto para grosor de espalda.',
                'muscle_group': 'back',
            },
            {
                'name': 'Lat Pulldown',
                'description': 'Jalón al pecho en polea alta. Alternativa a dominadas.',
                'muscle_group': 'back',
            },
            {
                'name': 'Deadlift',
                'description': 'Peso muerto convencional. Ejercicio compuesto total del cuerpo.',
                'muscle_group': 'back',
            },
            
            # PIERNAS
            {
                'name': 'Squat (Barra)',
                'description': 'Sentadilla con barra. Rey de los ejercicios de pierna.',
                'muscle_group': 'legs',
            },
            {
                'name': 'Romanian Deadlift',
                'description': 'Peso muerto rumano. Énfasis en isquiotibiales y glúteos.',
                'muscle_group': 'legs',
            },
            {
                'name': 'Leg Press',
                'description': 'Prensa de piernas. Ejercicio compuesto en máquina.',
                'muscle_group': 'legs',
            },
            {
                'name': 'Leg Curl',
                'description': 'Curl femoral. Aislamiento de isquiotibiales.',
                'muscle_group': 'legs',
            },
            {
                'name': 'Leg Extension',
                'description': 'Extensión de cuádriceps. Aislamiento de cuádriceps.',
                'muscle_group': 'legs',
            },
            
            # HOMBROS
            {
                'name': 'Overhead Press (Barra)',
                'description': 'Press militar con barra. Ejercicio compuesto de hombros.',
                'muscle_group': 'shoulders',
            },
            {
                'name': 'Lateral Raise',
                'description': 'Elevaciones laterales con mancuernas. Aislamiento de deltoides lateral.',
                'muscle_group': 'shoulders',
            },
            {
                'name': 'Face Pull',
                'description': 'Jalones a la cara en polea. Deltoides posterior y salud del hombro.',
                'muscle_group': 'shoulders',
            },
            
            # BRAZOS
            {
                'name': 'Barbell Curl',
                'description': 'Curl de bíceps con barra. Ejercicio básico de bíceps.',
                'muscle_group': 'arms',
            },
            {
                'name': 'Tricep Dips',
                'description': 'Fondos en paralelas para tríceps.',
                'muscle_group': 'arms',
            },
            {
                'name': 'Overhead Tricep Extension',
                'description': 'Extensión de tríceps sobre la cabeza.',
                'muscle_group': 'arms',
            },
            {
                'name': 'Hammer Curl',
                'description': 'Curl martillo con mancuernas. Énfasis en braquial.',
                'muscle_group': 'arms',
            },
            
            # CORE
            {
                'name': 'Plank',
                'description': 'Plancha isométrica. Fortalecimiento de core.',
                'muscle_group': 'core',
            },
            {
                'name': 'Hanging Leg Raise',
                'description': 'Elevaciones de piernas colgado. Ejercicio avanzado de abdominales.',
                'muscle_group': 'core',
            },
            {
                'name': 'Russian Twist',
                'description': 'Giros rusos. Trabajo de oblicuos.',
                'muscle_group': 'core',
            },
            
            # CARDIO
            {
                'name': 'Running',
                'description': 'Carrera continua o intervalos.',
                'muscle_group': 'cardio',
            },
            {
                'name': 'Cycling',
                'description': 'Bicicleta estática o de ruta.',
                'muscle_group': 'cardio',
            },
            {
                'name': 'Jump Rope',
                'description': 'Salto de cuerda. Cardio de alta intensidad.',
                'muscle_group': 'cardio',
            },
        ]

        created_count = 0
        for exercise_data in exercises_data:
            exercise, created = Exercise.objects.get_or_create(
                name=exercise_data['name'],
                is_global=True,
                defaults={
                    'description': exercise_data['description'],
                    'muscle_group': exercise_data['muscle_group'],
                    'created_by': None,
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Creado: {exercise.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Ya existe: {exercise.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Proceso completado. {created_count} ejercicios nuevos creados.')
        )