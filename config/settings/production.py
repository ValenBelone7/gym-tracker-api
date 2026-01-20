import os
import dj_database_url
from .base import *

# Debug
DEBUG = False

# Secret Key
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    '***REMOVED***'  # Fallback si no está en variables
)

# Allowed Hosts
ALLOWED_HOSTS = [
    'gym-tracker-backend.up.railway.app',
    '.railway.app',
    'localhost',
]

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    'https://gym-tracker-frontend.vercel.app',
    'https://gym-tracker-frontend-git-main-valenbelone7s-projects.vercel.app',
    'https://gym-tracker-frontend-30gyt6d80-valenbelone7s-projects.vercel.app',
    'http://localhost:5173',
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Static Files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security
CSRF_TRUSTED_ORIGINS = [
    'https://gym-tracker-backend.up.railway.app',
    'https://gym-tracker-frontend.vercel.app',
    'https://gym-tracker-frontend-git-main-valenbelone7s-projects.vercel.app',
    'https://gym-tracker-frontend-30gyt6d80-valenbelone7s-projects.vercel.app',
]

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Logging para debug
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

print("✅ Production settings loaded successfully")