set -e
echo "======================================"
echo "🚀 STARTING DJANGO APPLICATION"
echo "======================================"
echo "📊 Environment Check:"
echo "  PORT: $PORT"
echo "  DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
echo "  DATABASE_URL exists: $(if [ -n "$DATABASE_URL" ]; then echo 'YES'; else echo 'NO'; fi)"
echo ""
echo "🔄 Running migrations..."
python manage.py migrate --noinput
echo ""
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput --clear || echo "⚠️  Static collection failed (non-critical)"
echo ""
echo "🧪 Testing WSGI import..."
python -c "from config.wsgi import application; print('✅ WSGI loaded successfully')"
echo ""
echo "🚀 Starting Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --threads 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --capture-output