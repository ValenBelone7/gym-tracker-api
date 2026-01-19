"""
Django settings module selector.
Auto-detecta el ambiente correcto.
"""

import os

# Leer de variable de entorno
ENVIRONMENT = os.getenv('DJANGO_SETTINGS_MODULE', 'config.settings.development')

# Importar el módulo correcto
if 'production' in ENVIRONMENT:
    from .production import *
elif 'development' in ENVIRONMENT:
    from .development import *
else:
    # Fallback a development
    from .development import *