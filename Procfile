# Procfile for Railway deployment
# Note: With custom Dockerfile, migrations and collectstatic run in docker-entrypoint.sh
# This file is kept for compatibility but the Dockerfile handles the build

web: gunicorn --bind 0.0.0.0:$PORT --chdir src config.wsgi:application