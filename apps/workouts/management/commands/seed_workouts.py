"""
Comando de management para poblar entrenamientos de ejemplo.
Uso: `python manage.py seed_workouts` — añade datos iniciales para desarrollo.
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Seed the database with example workouts (development only)'

    def handle(self, *args, **options):
        # Implementar la lógica de seed aquí
        self.stdout.write(self.style.SUCCESS('seed_workouts: not implemented'))
