import os
import dj_database_url
from .base import *

print("🚀 Loading production settings...")

# Debug
DEBUG = False

# Secret Key
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is required")

# Allowed Hosts
ALLOWED_HOSTS = [
    'gym-tracker-backend.up.railway.app',
    '.railway.app',
    'localhost',
]

# Database
database_url = os.getenv('DATABASE_URL')
print(f"📊 DATABASE_URL exists: {bool(database_url)}")

if not database_url:
    raise ValueError("DATABASE_URL environment variable is not set!")

DATABASES = {
    'default': dj_database_url.config(
        default=database_url,
        conn_max_age=600,
        conn_health_checks=True,
    )
}

print(f"✅ Database configured: {DATABASES['default']['ENGINE']}")

# CORS - Solo agregar si no está en INSTALLED_APPS
if 'corsheaders' not in INSTALLED_APPS:
    INSTALLED_APPS += ['corsheaders']

# CORS debe estar PRIMERO en MIDDLEWARE
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

# Static Files - Simplificado y robusto
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Whitenoise configuration
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

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

print("✅ Production settings loaded successfully")