FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create staticfiles directory
RUN mkdir -p staticfiles

# Set environment variable
ENV PYTHONUNBUFFERED=1

# Run with explicit error handling
CMD set -e && \
    echo "Starting migrations..." && \
    python manage.py migrate --noinput && \
    echo "Collecting static files..." && \
    python manage.py collectstatic --noinput --clear || echo "Static collection failed, continuing..." && \
    echo "Starting gunicorn..." && \
    exec gunicorn config.wsgi:application \
        --bind 0.0.0.0:$PORT \
        --workers 2 \
        --threads 4 \
        --timeout 120 \
        --access-logfile - \
        --error-logfile - \
        --log-level debug \
        --capture-output