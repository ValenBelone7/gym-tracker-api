"""
URL Configuration principal.

Estructura:
- /admin/           → Django admin
- /api/auth/        → Autenticación (register, login, logout, me)
- /api/exercises/   → CRUD de ejercicios
- /api/routines/    → (futuro)
- /api/workouts/    → (futuro)
- /api/ai/          → (futuro)
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.exercises.urls')),
    path('api/', include('apps.routines.urls')),
    path('api/', include('apps.workouts.urls')),
    # path('api/', include('apps.ai_coach.urls')),      # Próximamente
]

# Servir media files en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Personalizar admin
admin.site.site_header = 'Gym Tracker Admin'
admin.site.site_title = 'Gym Tracker'
admin.site.index_title = 'Administración'