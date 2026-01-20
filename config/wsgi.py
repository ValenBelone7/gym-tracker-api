import os
import sys
from django.core.wsgi import get_wsgi_application

print("=" * 50)
print("🔍 WSGI Loading...")
print(f"Python version: {sys.version}")
print(f"Django settings: {os.getenv('DJANGO_SETTINGS_MODULE')}")
print("=" * 50)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

try:
    application = get_wsgi_application()
    print("✅ WSGI application loaded successfully")
except Exception as e:
    print(f"❌ WSGI Error: {e}")
    import traceback
    traceback.print_exc()
    raise