import os
import dj_database_url
from .base import *

# Debug
DEBUG = False
print("🚀 Production settings loaded")  # ← Para confirmar en logs

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

# CORS (ya lo agregaste)
INSTALLED_APPS += ['corsheaders']

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
    "https://gym-tracker-frontend.vercel.app",
    "http://localhost:5173",
]

CORS_ALLOW_CREDENTIALS = True

# Static
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security
CSRF_TRUSTED_ORIGINS = [
    'https://gym-tracker-backend.up.railway.app',
    'https://gym-tracker-frontend.vercel.app',
]

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')