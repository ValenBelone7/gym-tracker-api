#!/usr/bin/env python
import sys
import os

print("=" * 60)
print("🔍 DIAGNOSTIC SCRIPT")
print("=" * 60)

# Check Python version
print(f"✓ Python: {sys.version}")

# Check environment variables
print(f"✓ DJANGO_SETTINGS_MODULE: {os.getenv('DJANGO_SETTINGS_MODULE')}")
print(f"✓ DATABASE_URL exists: {bool(os.getenv('DATABASE_URL'))}")
print(f"✓ PORT: {os.getenv('PORT', 'NOT SET')}")

# Try importing Django
try:
    import django
    print(f"✓ Django version: {django.get_version()}")
except Exception as e:
    print(f"✗ Django import failed: {e}")
    sys.exit(1)

# Try setting up Django
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
    django.setup()
    print("✓ Django setup successful")
except Exception as e:
    print(f"✗ Django setup failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Try importing wsgi
try:
    from config.wsgi import application
    print("✓ WSGI application loaded")
except Exception as e:
    print(f"✗ WSGI import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=" * 60)
print("✅ ALL CHECKS PASSED")
print("=" * 60)