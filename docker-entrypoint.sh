#!/bin/bash
# Docker entrypoint script for VLE User Management System
# Runs migrations and collectstatic before starting the application

set -e

echo "Starting VLE User Management System..."

# Wait for database to be ready (optional but recommended)
echo "Waiting for database..."
until python src/manage.py check --database default > /dev/null 2>&1; do
  echo "Database is unavailable - sleeping"
  sleep 2
done

echo "Database is up!"

# Run migrations
echo "Running database migrations..."
python src/manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python src/manage.py collectstatic --noinput

echo "Starting application..."

# Execute the main command (gunicorn)
exec gunicorn --bind 0.0.0.0:${PORT:-8000} --chdir src config.wsgi:application
